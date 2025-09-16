import asyncio
import pprint
from concurrent.futures.thread import ThreadPoolExecutor
from multiprocessing.pool import ThreadPool
from typing import List, Dict
# from ..utils.async_fetcher import fetch_page_content, is_same_domain
# from ..utils.priority_queue import PriorityQueue
from config import settings
from Bilibili_Crawler import *
from Zhihu_Crawler import *


async def search_across_sites(query: str) -> List[Dict]:
    if not query.strip():
        return []

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(max_workers=2) as executor:  # 同步上下文管理器
        # 将同步函数转为异步任务
        tasks = [
            loop.run_in_executor(executor, bilibili_crawler, query),
            loop.run_in_executor(executor, zhihu_crawler, query)
        ]
        site_results = await asyncio.gather(*tasks)
        print(site_results)
    # 合并结果
    return site_results

if __name__ == '__main__':
    result = asyncio.run(search_across_sites('AX210网卡怎么样'))
    pprint.pprint(result)