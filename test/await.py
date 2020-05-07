import asyncio
import time
import requests

now = lambda: time.time()


async def do_some_work(x):
    print('Waiting: ', x)
    await asyncio.sleep(x)
    await requests.get('http://www.baidu.com')
    return 'Done after {}s'.format(x)


start = now()

coroutine = do_some_work(2)
loop = asyncio.get_event_loop()
task = asyncio.ensure_future(coroutine)
loop.run_until_complete(task)

print('Task ret: ', task.result())
print('TIME: ', now() - start)
