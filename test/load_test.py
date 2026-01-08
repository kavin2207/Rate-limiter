import asyncio
import aiohttp
import time
from collections import Counter

# ================= CONFIG =================
URL = "http://localhost:8000/orders"
TOTAL_REQUESTS = 10_000
CONCURRENCY = 200  # increase to 500 if your machine allows
HEADERS = {
    "X-User-Id": "user123",
    "Content-Type": "application/json",
    "Connection": "close",
}
PAYLOAD = {"item": "book", "qty": 1}
# ==========================================


async def worker(semaphore, session, stats):
    async with semaphore:
        try:
            async with session.post(URL, json=PAYLOAD, headers=HEADERS) as resp:
                stats[resp.status] += 1
        except Exception:
            stats["error"] += 1


async def main():
    semaphore = asyncio.Semaphore(CONCURRENCY)
    stats = Counter()

    timeout = aiohttp.ClientTimeout(total=10)
    connector = aiohttp.TCPConnector(limit=CONCURRENCY)

    start = time.time()

    async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
        tasks = [worker(semaphore, session, stats) for _ in range(TOTAL_REQUESTS)]
        await asyncio.gather(*tasks)

    elapsed = time.time() - start

    print("\n========= LOAD TEST RESULT =========")
    print(f"Total requests : {TOTAL_REQUESTS}")
    print(f"Concurrency    : {CONCURRENCY}")
    print(f"Time taken    : {elapsed:.2f} sec")
    print(f"Throughput    : {TOTAL_REQUESTS / elapsed:.2f} req/sec")
    print("----------------------------------")
    for k, v in sorted(stats.items()):
        print(f"{k}: {v}")
    print("==================================\n")


if __name__ == "__main__":
    asyncio.run(main())
