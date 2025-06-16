from hash_ring import ConsistentHashRing

ring = ConsistentHashRing()

# Add 3 servers
ring.add_server(1)
ring.add_server(2)
ring.add_server(3)

# Simulate 10 request IDs
print("Request ID → Server")
for rid in range(10):
    server = ring.get_server(rid)
    print(f"{rid} → Server {server}")
