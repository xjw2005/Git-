from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import aiohttp
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import asyncio
from typing import List, Dict

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 托管前端静态文件
app.mount("/static", StaticFiles(directory="static"), name="static")

# 要搜索的固定网站列表
TARGET_WEBSITES = [
    "https://zh.wikipedia.org",
    "https://www.zhihu.com",
    "https://www.bilibili.com",
    "https://github.com",
    "https://stackoverflow.com"
]


async def fetch_page_content(url: str, session: aiohttp.ClientSession) -> Dict:
    """获取单个页面内容"""
    try:
        async with session.get(url, timeout=10) as response:
            if response.status == 200:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # 移除不需要的元素
                for element in soup(['script', 'style', 'nav', 'footer', 'iframe']):
                    element.decompose()

                title = soup.title.string if soup.title else url
                content = ' '.join(soup.stripped_strings)

                return {
                    'url': url,
                    'title': title,
                    'content': content
                }
            return None
    except Exception as e:
        print(f"Error fetching {url}: {str(e)}")
        return None


async def search_website(base_url: str, query: str, session: aiohttp.ClientSession, max_pages: int = 3) -> List[Dict]:
    """在单个网站内搜索关键词"""
    results = []
    visited = set()
    queue = [base_url]

    while queue and len(results) < max_pages:
        url = queue.pop(0)

        if url in visited:
            continue
        visited.add(url)

        page_data = await fetch_page_content(url, session)
        if not page_data:
            continue

        # 检查是否包含关键词
        if query.lower() in page_data['content'].lower():
            results.append(page_data)

        # 提取新链接 (仅限同域名)
        if len(results) < max_pages:  # 只有结果不足时才继续爬取
            soup = BeautifulSoup(page_data['content'], 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                absolute_url = urljoin(base_url, href)
                if (urlparse(absolute_url).netloc == urlparse(base_url).netloc and
                        absolute_url not in visited and
                        absolute_url not in queue):
                    queue.append(absolute_url)

        # 礼貌延迟
        await asyncio.sleep(1)

    return results


@app.get("/api/search")
async def search(query: str, max_results: int = 10):
    """搜索接口"""
    if not query:
        return []

    all_results = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for website in TARGET_WEBSITES:
            tasks.append(search_website(website, query, session))

        website_results = await asyncio.gather(*tasks)
        for site_results in website_results:
            all_results.extend(site_results)

    # 简单排序 - 按关键词出现次数
    sorted_results = sorted(
        all_results,
        key=lambda x: x['content'].lower().count(query.lower()),
        reverse=True
    )

    return sorted_results[:max_results]


@app.get("/")
async def serve_frontend():
    """提供前端页面"""
    with open("./static/index.html", "r", encoding="utf-8") as f:
        return Response(content=f.read(), media_type="text/html")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)