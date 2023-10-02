import aiohttp
import asyncio

async def post(url, key):
    async with aiohttp.ClientSession() as session:
        async with await session.put(url, data={'tg_id': key}) as resp:
            return resp.status
