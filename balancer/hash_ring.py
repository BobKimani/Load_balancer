import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, num_slots=512, virtual_nodes=9):
        self.num_slots = num_slots
        self.virtual_nodes = virtual_nodes
        self.ring = {}  # slot index -> server_id
        self.sorted_keys = []  # sorted list of slot indices

    def _hash(self, key):
        """Generic hash function using MD5 + modulo ring size"""
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16) % self.num_slots

    def _server_hash(self, i, j):
        """Φ(i, j) = i + j + 2^j + 25"""
        return (i + j + (2 ** j) + 25) % self.num_slots

    def _request_hash(self, i):
        """H(i) = i + 2^i + 17"""
        return (i + (2 ** i) + 17) % self.num_slots

    def add_server(self, server_id):
        """Add virtual replicas of a physical server"""
        for j in range(self.virtual_nodes):
            slot = self._server_hash(server_id, j)

            # Resolve collision via linear probing
            while slot in self.ring:
                slot = (slot + 1) % self.num_slots

            self.ring[slot] = server_id
            bisect.insort(self.sorted_keys, slot)

    def remove_server(self, server_id):
        """Remove all virtual nodes of a server"""
        keys_to_remove = [slot for slot, sid in self.ring.items() if sid == server_id]
        for slot in keys_to_remove:
            del self.ring[slot]
            self.sorted_keys.remove(slot)

    def get_server(self, request_id):
        """Get server for a given request id using clockwise lookup"""
        try:
            i = int(request_id)
        except:
            i = sum([ord(c) for c in str(request_id)])
        hash_val = self._request_hash(i)

        idx = bisect.bisect(self.sorted_keys, hash_val)
        if idx == len(self.sorted_keys):
            idx = 0  # wrap around
        return self.ring[self.sorted_keys[idx]]

