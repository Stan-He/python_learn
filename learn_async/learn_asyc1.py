#!/usr/bin/env python3
# countasync.py
# async multi-function

# await代表将控制权交回给event loop
# async def 声明的function是一个协程，协程使用await、yeild、return都可以
# async def + yield声明的generator，可以使用async for调用、不能使用yield from
# await只能使用在async def声明的函数里面
# 如果await一个函数，那么这个函数也必须是awaitable的

import asyncio

async def count():
    print("One")
    await asyncio.sleep(1)
    print("Two")

async def count1():
    print("One-1")
    await asyncio.sleep(0.5)
    print("Two-1")
    await asyncio.sleep(0.5)
    print("Three-1")

async def count2():
    print("One-2")
    return "c2 complete"

async def count3():
    for i in range(3):
        yield 100+i

async def count4():
    print("count4-1")
    await asyncio.sleep(0.2)
    print("count4-2")

async def count5():
    print("count5-1")
    await asyncio.sleep(0.6)
    await count4()
    print("count5-2")

async def main():
    #main wait for 3 count
    await asyncio.gather(count2(),count(), count(), count(),count1(),count5())
    async for i in count3():
        print(i)

if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")