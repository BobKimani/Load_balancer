from flask import Flask, jsonify, request
import requests
from hash_ring import ConsistentHashRing
import subprocess

app = Flask(__name__)
ring = ConsistentHashRing()
replicas = {
    1: "server1",
    2: "server2",
    3: "server3"
}

# Register servers to the hash ring
for sid in replicas:
    ring.add_server(sid)

@app.route("/rep", methods=["GET"])
def get_replicas():
    return jsonify({
        "message": {
            "N": len(replicas),
            "replicas": [f"Server {sid}" for sid in replicas]
        },
        "status": "successful"
    }), 200

@app.route("/home", methods=["GET"])
def route_home():
    # Use client IP hash as request ID
    request_id = str(hash(request.remote_addr))[-6:]
    server_id = ring.get_server(int(request_id))
    port = replicas.get(server_id)

    try:
        res = requests.get(f"http://server{server_id}:5000/home")
        return jsonify(res.json()), 200
    except Exception as e:
        return jsonify({"message": "Server unavailable", "error": str(e)}), 500

@app.route('/add', methods=['POST'])
def add_servers():
    try:
        data = request.get_json()
        n = data.get("n")
        hostnames = data.get("hostnames")

        if not n or not hostnames or len(hostnames) != n:
            return jsonify({"error": "Invalid input"}), 400

        for i in range(n):
            hostname = hostnames[i]
            server_id = len(ring.servers) + 1
            container_name = f"server{server_id}"
            port = 5000

            # Start Docker container
            subprocess.run([
                "docker", "run", "-d",
                "--name", container_name,
                "--network", "load_balancer_net1",
                "-e", f"SERVER_ID={server_id}",
                "server"
            ], check=True)

            # Register in the hash ring
            ring.add_server(server_id)

        return jsonify({"message": f"{n} servers added.", "servers": hostnames}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
