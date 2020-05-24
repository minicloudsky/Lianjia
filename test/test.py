import asyncio
import time

now = lambda: time.time()


async def do_some_work(x):
    print("Waiting: ", x)


start = now()
coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
loop.run_until_complete(coroutine)
print("TIME: ", now() - start)
