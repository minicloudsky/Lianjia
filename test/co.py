import time
import asyncio


async def show(num):
    print("Number is {}".format(num))
    # await asyncio.sleep(1)
    time.sleep(1)

start = time.time()
tasks = [asyncio.ensure_future(show(i)) for i in range(1, 6)]
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
end = time.time()
print("Cost time:", end - start, "aaa")
