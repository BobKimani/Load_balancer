from flask import Flask, request, jsonify
import requests
import os
import threading
import time

from hash_ring import ConsistentHashRing

app = Flask(__name__)
ring = ConsistentHashRing()

# Initial servers (assumes 3 are already running)
for i in range(1, 4):  # Server IDs: 1, 2, 3
    ring.add_server(i)


@app.route('/home', methods=['GET'])
def route_request():
    try:
        req_id = int(request.args.get("id", 0))
        server = ring.get_server(req_id)
        port = 5000
        host = f"http://server{server}:{port}/home"
        res = requests.get(host)

        return jsonify(res.json()), res.status_code
    except Exception as e:
        return jsonify({"error": str(e), "message": "Server unavailable"}), 500


@app.route('/rep', methods=['GET'])
def get_replicas():
    return jsonify({
        "message": {
            "N": len(ring.servers),
            "replicas": [f"Server {s}" for s in ring.servers]
        },
        "status": "successful"
    })


@app.route('/add', methods=['POST'])
def add_servers():
    try:
        data = request.get_json()
        n = data.get("n")
        hostnames = data.get("hostnames")

        if not n or not hostnames or len(hostnames) != n:
            return jsonify({"error": "Invalid input"}), 400

        created = []

        for i in range(n):
            hostname = hostnames[i]
            server_id = len(ring.servers) + 1

            print(f"[INFO] Please start container: server{server_id} with SERVER_ID={server_id}")

            ring.add_server(server_id)
            created.append(f"server{server_id}")

        return jsonify({
            "message": f"{n} servers added to hash ring. Start containers manually.",
            "servers": created
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/rm', methods=['POST'])
def remove_servers():
    try:
        data = request.get_json()
        ids = data.get("ids")

        if not ids or not isinstance(ids, list):
            return jsonify({"error": "Invalid input, expected list of server IDs"}), 400

        removed = []

        for server_id in ids:
            if server_id in ring.servers:
                ring.remove_server(server_id)
                print(f"[INFO] Please stop container: server{server_id}")
                removed.append(f"server{server_id}")
            else:
                print(f"[WARN] Server {server_id} not found in hash ring.")

        return jsonify({
            "message": f"{len(removed)} servers removed from hash ring. Stop containers manually.",
            "servers": removed
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def heartbeat(interval=10):
    while True:
        time.sleep(interval)
        for server_id in ring.servers.copy():
            try:
                host = f"http://server{server_id}:5000/home"
                res = requests.get(host, timeout=2)
                if res.status_code != 200:
                    raise Exception(f"Bad status {res.status_code}")
            except Exception:
                print(f"[HEARTBEAT] Server {server_id} unreachable. Removing from hash ring.")
                ring.remove_server(server_id)


if __name__ == '__main__':
    threading.Thread(target=heartbeat, daemon=True).start()
    app.run(host='0.0.0.0', port=5000)
