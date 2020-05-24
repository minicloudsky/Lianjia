import aiohttp
import asyncio
import redis
import json


async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()


async def main():
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, 'http://www.baidu.com')
        # print(html)
    return html


async def save():
    r = redis.Redis(host='', port=6379, password='')
    html = await  main()
    r.set("html", json.dumps(html))


loop = asyncio.get_event_loop()
loop.run_until_complete(save())
