import asyncio
import pprint
from typing import List, Dict
# from ..utils.async_fetcher import fetch_page_content, is_same_domain
# from ..utils.priority_queue import PriorityQueue
from config import settings
from Bilibili_Crawler import *
from Zhihu_Crawler import *


async def search_single_site(
        base_url: str,
        query: str,
        session: aiohttp.ClientSession,
        max_pages: int = 3
) -> List[Dict]:
    """在单个网站内执行关键词搜索"""
    results = []
    queue = PriorityQueue()
    queue.add(base_url, priority=10)  # 首页高优先级

    while not queue.is_empty() and len(results) < max_pages:
        current_url = queue.pop()

        page_data = await fetch_page_content(current_url, session)
        if not page_data:
            continue

        # 关键词匹配检查
        content_lower = page_data['content'].lower()
        if query.lower() in content_lower:
            # 计算关键词密度作为排序依据
            keyword_count = content_lower.count(query.lower())
            page_data['relevance'] = keyword_count / len(content_lower.split())
            results.append(page_data)

        # 提取新链接
        soup = BeautifulSoup(page_data['raw_html'], 'html.parser')
        for link in soup.find_all('a', href=True):
            href = link['href']
            absolute_url = urljoin(base_url, href)

            if is_same_domain(base_url, absolute_url):
                # 根据链接文本判断优先级
                link_text = link.get_text().lower()
                priority = 5  # 默认优先级
                if query.lower() in link_text:
                    priority = 8  # 含关键词的链接更高优先级
                elif 'login' in link_text:
                    priority = 0  # 登录页跳过

                queue.add(absolute_url, priority=priority)

        await asyncio.sleep(1)  # 礼貌延迟

    return results


async def search_across_sites(
        query: str
) -> List[Dict]:
    """跨多个目标网站搜索关键词"""
    if not query.strip():
        return []

    async with aiohttp.ClientSession() as session:
        task1 = bilibili_crawler(query)
        task2 = zhihu_crawler(query)

        tasks = [task1, task2]

        # 并行执行所有站点搜索
        site_results = await asyncio.gather(*tasks)

        # 合并并排序结果
        all_results = []
        for results in site_results:
            all_results.extend(results)

        # 按相关性排序
        # sorted_results = sorted(
        #     all_results,
        #     key=lambda x: x['relevance'],
        #     reverse=True
        # )

        return all_results

if __name__ == '__main__':
    result = asyncio.run(search_across_sites('AX210网卡怎么样'))
    pprint.pprint(result)