#!/usr/bin/env python3
# rand.py

import asyncio
import random

# ANSI colors
c = (
    "\033[0m",   # End of color
    "\033[36m",  # Cyan
    "\033[91m",  # Red
    "\033[35m",  # Magenta
)

async def makerandom(idx: int, threshold: int = 6) -> int:
    """
    输入idx代表颜色，
    """
    print(c[idx + 1] + f"Initiated makerandom({idx}).")
    i = random.randint(0, 9)
    while i <= threshold:
        print(c[idx + 1] + f"makerandom({idx}) == {i} too low; retrying.")
        await asyncio.sleep(0.5)
        i = random.randint(0, 9)
    print(c[idx + 1] + f"---> Finished: makerandom({idx}) == {i}" + c[0])
    return i

async def main():
    #res = await asyncio.gather(*(makerandom(i, 10 - i - 1) for i in range(3)))
    res = await asyncio.gather(makerandom(0, 8),makerandom(1, 8),makerandom(2, 8) )
    return res

if __name__ == "__main__":
    random.seed(444)
    r1, r2, r3 = asyncio.run(main())
    print()
    print(f"r1: {r1}, r2: {r2}, r3: {r3}")