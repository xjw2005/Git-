import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import pprint

#数据结构

title = None
link = None
message = None
data = {"标题": title ,
        "介绍：":message,
        "链接": link
        }

#


if __name__ == '__main__':
    # 自动打开浏览器
    os.popen('"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium\ChromeProfile"')
    result_list = []