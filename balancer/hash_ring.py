import hashlib
import bisect

class ConsistentHashRing:
    def __init__(self, num_slots=2048, virtual_nodes=350):
        self.num_slots = num_slots
        self.virtual_nodes = virtual_nodes
        self.ring = {}  # slot index -> server_id
        self.sorted_keys = []  # sorted list of slot indices
        self.servers = []

    def _hash(self, key):
        """Generic hash function using MD5 + modulo ring size"""
        return int(hashlib.md5(str(key).encode()).hexdigest(), 16) % self.num_slots

    def _server_hash(self, server_id, vnode_index):
        """Generate a consistent virtual node hash for a server"""
        key = f"{server_id}-vn-{vnode_index}"
        return self._hash(key)

    def _request_hash(self, request_id):
        """Hash a request ID into the ring"""
        return self._hash(request_id)

    def add_server(self, server_id):
        if server_id in self.servers:
            return
        self.servers.append(server_id)

        for j in range(self.virtual_nodes):
            index = self._server_hash(server_id, j)
            # Ensure uniqueness in case of hash collisions
            while index in self.ring:
                index = (index + 1) % self.num_slots
            self.ring[index] = server_id
            bisect.insort(self.sorted_keys, index)

    def remove_server(self, server_id):
        """Remove all virtual nodes of a server"""
        keys_to_remove = [slot for slot, sid in self.ring.items() if sid == server_id]
        for slot in keys_to_remove:
            del self.ring[slot]
            self.sorted_keys.remove(slot)
        if server_id in self.servers:
            self.servers.remove(server_id)

    def get_server(self, request_id):
        """Get server for a given request id using clockwise lookup"""
        if not self.sorted_keys:
            raise Exception("No servers in the ring")
        try:
            key = int(request_id)
        except ValueError:
            key = sum([ord(c) for c in str(request_id)])

        hash_val = self._request_hash(key)
        idx = bisect.bisect(self.sorted_keys, hash_val)
        if idx == len(self.sorted_keys):
            idx = 0  # wrap around
        return self.ring[self.sorted_keys[idx]]

