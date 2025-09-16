from aiohttp.abc import HTTPException
from crawlers.single_crawler import single_crawler
from crawlers.Doubao_Crawler import doubao_crawler
from fastapi import FastAPI
from typing import Optional
import pathlib
from pydantic import BaseModel
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uvicorn


app = FastAPI(title="学习FastAPI",
              description="以下是关于FastAPI框架文档的介绍和描述",
              version="0.0.1")

templates = Jinja2Templates(directory=f"{pathlib.Path(__file__).parent}/templates/")

#使用app实例对象来装饰实现路由注册
class CrawlRequest(BaseModel):
    query: str
@app.post("/api/crawl")
async def crawl(request: CrawlRequest):
    """
    爬虫接口
    :param url:
    :return:
    """
    try:
        result_list = single_crawler(query= request.query)
        for item in result_list:
            if "bilibili.com" in item.get("链接:"):
                item["platform"] = "bilibili"
            elif "zhihu.com" in item.get("链接:"):
                item["platform"] = "zhihu"
            else:
                item["platform"] = "doubao"
        return result_list
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"爬虫执行失败：{str(e)}")
@app.get("/", response_class=HTMLResponse)
async  def get_resopnse(request: Request):
    return templates.TemplateResponse("index.html",
                                      {"request": request})



if __name__ == '__main__':
    app_modeel_name = os.path.basename(__file__).replace(".py", '')
    print(f'{app_modeel_name}')
    uvicorn.run(app=f'{app_modeel_name}:app', host="127.0.0.1", port=8000, reload=True)
