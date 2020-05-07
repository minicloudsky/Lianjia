import asyncio
import time

now = lambda: time.time()


async def do_some_work(x):
    print("Waiting: ", x)


start = now()
coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
# task = loop.create_task(coroutine)
task = asyncio.ensure_future(coroutine)
print(task)
print(isinstance(task, asyncio.Future))
loop.run_until_complete(task)
print(task)
print('TIME:', now() - start)
print(task.result())
