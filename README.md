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

### ✅ Expected Output (example):
```bash
Request ID → Server
0 → Server 3
1 → Server 2
2 → Server 1
 ...
```
- (Shows which server each request ID is routed to)

### 📸 Screenshot Suggestion:

