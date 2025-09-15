from typing import List

class Settings:
    APP_NAME = "Web Searcher"
    TARGET_WEBSITES: List[str] = [
        "https://zh.wikipedia.org",
        "https://www.zhihu.com",
        "https://www.bilibili.com",
        "https://github.com",
        "https://stackoverflow.com"
    ]
    REQUEST_TIMEOUT = 10
    MAX_CONCURRENT_REQUESTS = 5

settings = Settings()