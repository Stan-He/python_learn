#!/usr/bin/env python3
# countasync.py

import asyncio

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def count1():
    print("One-s")
    await asyncio.sleep(0.5)
    print("Two-s")
    await asyncio.sleep(0.5)
    print("Three-s")

async def main():
    #main wait for 3 count
    await asyncio.gather(count(), count(), count(),count1())

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")