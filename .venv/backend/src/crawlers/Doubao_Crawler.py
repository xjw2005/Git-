import time
from selenium.common import NoSuchElementException
from anyio import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import List, Dict
import subprocess
import psutil
import os
import pprint


def doubao_crawler(query: str = "AX1800pcie网卡是intel还是联发科的？", driver: webdriver.Chrome = None):
    print("开始抓取豆包：")
    try:
        driver.switch_to.window(driver.window_handles[0])
        driver.get("https://www.doubao.com/chat/")

        # 等待输入框可用并发送查询（使用显式等待）
        search_box = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//*[@id="chat-route-layout"]/div/main/div/div/div[2]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/div[1]/div/textarea'))
        )
        search_box.send_keys(f"{query}")
        search_box.send_keys(Keys.ENTER)
        start_time = time.time()
        prev_result = ""
        print("读取豆包结果...")
        while time.time() - start_time < 25:
            try:
                time.sleep(2)
                #                                             //*[@id="chat-route-layout"]/div/main/div/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div/div[1]
                result = driver.find_element(By.XPATH,
                                             '//*[@id="chat-route-layout"]/div/main/div/div/div[2]/div/div[1]/div/div/div[2]/div[2]/div/div/div/div/div/div/div[1]/div/div[1]').text
                if result == prev_result and result != '':
                    print("匹配成功得到的结果：")
                    break
                prev_result = result

            except Exception as e:
                continue

        # print(result)
        driver.switch_to.window(driver.window_handles[0])
        href = driver.current_url
        print(f"豆包链接：{href}")
        return {
            "标题:": "豆包内容",
            "链接:": f"{href}",
            "介绍:": result,
            "relevance": 0.5
        }
    except Exception as e:
        print(f"[Fetch Error] {query}: {str(e)}")


if __name__ == '__main__':
    options = Options()
    options.add_experimental_option("debuggerAddress", "localhost:9222")
    options.add_argument("--headless")  # 启用无头模式
    options.add_argument("--disable-gpu")  # 禁用 GPU 加速

    chrome_process = subprocess.Popen([
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "--remote-debugging-port=9222",
        "--user-data-dir=C:\\selenium\\ChromeProfile"
    ])

    # 创建Chrome WebDriver实例
    driver = webdriver.Chrome(options=options)

    doubao_crawler(driver= driver)