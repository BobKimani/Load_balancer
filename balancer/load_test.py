import requests
import matplotlib.pyplot as plt
from collections import Counter

NUM_REQUESTS = 10000

print("\n⏳ Sending test requests...")

counter = Counter()
errors = 0

for i in range(NUM_REQUESTS):
    try:
        res = requests.get(f"http://localhost:5000/home?id={i}")
        server = res.json()["message"].split(":")[-1].strip()
        counter[server] += 1
    except Exception:
        errors += 1

# 📊 Print distribution
print("\n📊 Request Distribution Summary")
for server, count in sorted(counter.items()):
    print(f"{server}: {count} requests")

# 🖼️ Plot
labels = list(counter.keys())
counts = list(counter.values())

plt.figure(figsize=(8, 5))
plt.bar(labels, counts, color='mediumpurple')
plt.title("Load Distribution Across Servers")
plt.xlabel("Server")
plt.ylabel("Number of Requests")
plt.tight_layout()
plt.savefig("load_distribution.png")  # Save for headless environments
print("Chart saved as load_distribution.png")

if errors:
    print(f"\n⚠️ Errors encountered: {errors}")

