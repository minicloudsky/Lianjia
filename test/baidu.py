import asyncio
import requests
import redis
import json


async def get_html():
    html = await  requests.get('http://www.baidu.com')
    return html


async def save_data():
    text = await get_html()
    r = redis.Redis()
    r.set('baidu', json.dumps(text))
    print("finish")


if __name__ == '__main__':
    coroutine = asyncio.ensure_future(save_data())
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(coroutine)
