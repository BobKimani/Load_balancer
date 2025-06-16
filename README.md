# Load Balancing

This is a simple Python Flask web server used in a Distributed Systems project. It is meant to act as a minimal backend server managed by a load balancer for load distribution using consistent hashing.

---

## 🛠️ Features

- Responds to `/home` endpoint with a unique server ID
- Responds to `/heartbeat` to signal it is alive
- Containerized using Docker
- SERVER_ID passed as environment variable

---

## 🔧 Endpoints

### `GET /home`

Returns a JSON response with a message showing the unique server ID.

```json
{
  "message": "Hello from Server: [ID]",
  "status": "successful"
}
