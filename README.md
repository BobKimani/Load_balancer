# Load Balancing

## 📌 Overview

This project implements a lightweight **load balancer** using **consistent hashing** and **Docker-based container orchestration**. It dynamically routes HTTP requests to backend servers and supports horizontal scaling via hashing logic.

All services (servers and balancer) are containerized and communicate using Docker’s internal network via Docker Compose.

---

## ✅ Task 1: Server Implementation

### 🔨 Features

- Lightweight Flask server exposing:
  - `GET /home` → `{"message": "Hello from Server: X", "status": "successful"}`
  - `GET /heartbeat` → 200 OK (for future health checks)
- Parameterized using `SERVER_ID` environment variable
- Dockerized for replication

### 📂 Location

- `server/server.py`
- `server/Dockerfile`

### 🧪 How to Test

```bash
curl http://localhost:5000/home
```

![image](https://github.com/user-attachments/assets/fdacebec-208f-4295-9222-90807b849d11)

## ✅ Task 2: Consistent Hashing Implementation & Testing

🔹 Consistent Hash Ring Details:
 - Ring size: 512
 - 9 virtual nodes per physical server
 - Request hash:      H(i)  = i + 2^i + 17
 - Virtual node hash: Φ(i,j) = i + j + 2^j + 25
 - Collision resolution: linear probing
 - Server lookup: clockwise search

### 🔹 Files Involved:
 - balancer/hash_ring.py       # Implements the ConsistentHashRing class
 - balancer/test_ring.py       # Test script for verifying server mapping

### 🧪 Run the test script to verify the consistent hashing behavior
```bash
python balancer/test_ring.py
```

### ✅ Expected Output:

![image](https://github.com/user-attachments/assets/6324c59d-24c4-4016-aaa7-e190490a9032)

- (Shows which server each request ID is routed to)


## Task 3: Dynamic Addition of Server Nodes
### Objective
- Implement dynamic scalability of the system by allowing new replica nodes to be added to the consistent hash ring at runtime without restarting the system.

### Key Implementation Details
- A new API endpoint /add (HTTP POST) was created in the load_balancer.py to allow runtime server additions.
- The consistent hash ring is updated to include new server IDs.
- The load balancer no longer attempts to start Docker containers directly (for security and portability reasons).

Instead, users are instructed to manually start containers on the host after the hash ring is updated.

### 🧪 Testing the /add Endpoint
- Use curl to add new server(s):
- 🐳 Manually Starting the New Server Container
  
### Screenshot of the manual starting of the new server container

![image](https://github.com/user-attachments/assets/824172bc-9900-4a61-8813-49f2b0e361ec)


