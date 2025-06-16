# Load Balancing

## Overview

This project implements a lightweight **load balancer** using **consistent hashing** and **Docker-based container orchestration**. It dynamically routes HTTP requests to backend servers and supports horizontal scaling via hashing logic.

All services (servers and balancer) are containerized and communicate using Docker’s internal network via Docker Compose.

---

##  Task 1: Server Implementation

###  Features

- Lightweight Flask server exposing:
  - `GET /home` → `{"message": "Hello from Server: X", "status": "successful"}`
  - `GET /heartbeat` → 200 OK (for future health checks)
- Parameterized using `SERVER_ID` environment variable
- Dockerized for replication

### Location

- `server/server.py`
- `server/Dockerfile`

###  How to Test

```bash
curl http://localhost:5000/home
```

![image](https://github.com/user-attachments/assets/fdacebec-208f-4295-9222-90807b849d11)

##  Task 2: Consistent Hashing Implementation & Testing

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

### Run the test script to verify the consistent hashing behavior
```bash
python balancer/test_ring.py
```

### Expected Output:

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

###  Testing the /add Endpoint
- Use curl to add new server(s):
- 🐳 Manually Starting the New Server Container
  
### Screenshot of the manual starting of the new server container

![image](https://github.com/user-attachments/assets/824172bc-9900-4a61-8813-49f2b0e361ec)


##  Task 4: Dynamic Removal of Server Nodes
### Objective
- Allow servers to be removed from the consistent hash ring at runtime without restarting the system, and notify the user to manually stop the corresponding Docker containers.

### Key Implementation Details
- Introduced a new API endpoint /rm (HTTP POST) in load_balancer.py.
- Accepts a list of server IDs to remove.
- Updates the consistent hash ring by removing the specified nodes.
- Prints console messages reminding the user to manually stop the containers.
- Ensures the system remains operational while scaling down.

### API Endpoint: /rm
Send a request with the server IDs you wish to remove:
![image](https://github.com/user-attachments/assets/b6bcba22-6291-474c-8e44-9d07a419a7bc)

### Manually Stop Docker Containers
After removing the server from the hash ring, stop and remove its container manually:

```bash
docker stop server3
docker rm server3
```

## Task 5: Failure Detection Using Heartbeats
- This task adds automatic failure detection for backend servers using a background heartbeat mechanism. The load balancer continuously monitors all active servers and removes any that become unresponsive from the consistent hash ring.

### Features Implemented
- A background thread periodically pings each backend server's /home endpoint.
- If a server fails to respond within a 2-second timeout, it is considered unavailable.
- The unresponsive server is removed from the consistent hash ring, ensuring no future requests are routed to it.
- This prevents request failures caused by inactive or crashed containers.

### Heartbeat Logic
- The heartbeat thread starts automatically when the load balancer runs:

![image](https://github.com/user-attachments/assets/0ba718b8-7ec5-4707-9c02-fa5f62036434)

### How to Test
- Start the system.
- Stop one of the backend servers.
- Wait ~10 seconds for the heartbeat to detect failure.
- Check current replicas:
  
  ![image](https://github.com/user-attachments/assets/b0b4faea-58b0-4aba-a4b0-c26b897a5d5c)

- You must manually stop or restart Docker containers as needed.

# Conclusions
- The API Summary

![image](https://github.com/user-attachments/assets/81b9b56b-50a3-4f7d-8467-a367ebb4e2d8)




