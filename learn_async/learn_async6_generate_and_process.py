import asyncio
from asyncio import tasks
from concurrent.futures import process
import datetime


def main():
    loop = asyncio.get_event_loop()

    t0 = datetime.datetime.now()

    data = asyncio.Queue()

    task = asyncio.gather(
        generate_data(10,data),
        generate_data(10,data),
        process_data(5,data),
        process_data(5,data),
        process_data(5,data),
        process_data(5,data),
    )

    loop.run_until_complete(task)

async def generate_data(num, data):
    for idx in range(0,num + 1):
        item = idx * idx
        work = (item,datetime.datetime.now())
        await data.put(work)
        print(f"------- generated item:{item}")

        await asyncio.sleep(0.5)


async def process_data(num: int, data: asyncio.Queue):
    processed = 0
    while processed < num:
        item = await data.get()
        # item is a corotine
        processed +=1
        values = item[0]
        t= item[1]
        dt = datetime.datetime.now() -t
        print(f"++++ Processed value: {values} after {dt.total_seconds()} sec")
        await asyncio.sleep(0.5)

main()