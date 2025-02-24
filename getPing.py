import asyncio
from typing import List, Optional
from aiohttp import ClientSession, ClientTimeout
import time


async def __get_real_ping_time(url: str, proxy: Optional[str] = None, download_timeout:int =  10) -> int:
    response_time = -1
    try:
        timeout = ClientTimeout(total=download_timeout)

        async with ClientSession(timeout=timeout) as session:
            start_time = time.time()
            async with session.get(url, proxy=proxy) as response:
                await response.read()
                end_time = time.time()
                elapsed_time = end_time - start_time
                response_time = int(elapsed_time * 1000)
    except Exception as ex:
        # print(f"Exception occurred for {url} with proxy {proxy}: {ex}")
        pass
    return response_time


async def __test_urls_with_proxies(urls: List[str], proxies: List[Optional[str]], download_timeout):
    tasks = []

    for url in urls:
        for proxy in proxies:
            tasks.append(__get_real_ping_time(url, proxy, download_timeout))

    results = await asyncio.gather(*tasks)

    return results


async def testPing(testUrl=['https://www.google.com/generate_204'], proxies=[], timeout=10):

    results = await __test_urls_with_proxies(testUrl, proxies, timeout)
    testedList = []
    results_index = 0
    for _ in testUrl:
        for proxy in proxies:
            ping_time = results[results_index]
            testedList.append(ping_time)
            results_index += 1
    return testedList


