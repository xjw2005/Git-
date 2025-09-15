import time
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import psutil
import subprocess
import pprint


#自动打开浏览器
chrome_process = subprocess.Popen([
        "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "--remote-debugging-port=9222",
        "--user-data-dir=C:\\selenium\\ChromeProfile"
    ])
#数据
result_list = []
title = None
link = None
message = None
data = {"标题": title ,
        "介绍：":message,
        "链接": link
        }

options = Options()
options.add_experimental_option("debuggerAddress", "localhost:9222")
options.add_argument("--headless")  # 启用无头模式
options.add_argument("--disable-gpu")  # 禁用 GPU 加速

#创建Chrome WebDriver实例
driver = webdriver.Chrome(options=options)
# driver.add_cookie({'Cookie':'_xsrf=6gr2Af9NZBGZT3jDUAstKY10otzam63Q; __zse_ck=004_W9MC6y4Bxk1Sl9LboZgVWBXv6ymOYOSO0pqt26UOFu15EoUybXjhY5g8h8YV6ESG=aAi482czJsV169RNeI=wByscqS1dshY7UTmgGBxc2ze0AsVxKQqzRDOerAog5eT-VMtLfvW8QS5Lq+fsjfjkWs/3rRpPuSANpqVVW/hBCe86AYpkqsqIv6Nn+wg/vuYVy1O3tHzoONnw0UZOVQO2Nu7A+irHf9LDkLaSN0Ic6t6tw/jjvjxZYIkUNhzW11Xh; _zap=82dfae0b-2608-4bf9-8c16-810ad145de26; d_c0=-6ATL3aY-BqPTlm37W1YHtC2T9BkqkS9T_8=|1756139563; captcha_session_v2=2|1:0|10:1757002234|18:captcha_session_v2|88:bklJZUdOUVRtblNOU1FRM0RzaWxJdDB4ZERuQ3hrUmhmZ2xmWXdRS3BzUE80OEU0UTROYlZvWTR6eGs2NkJDWg==|1134a79b0cd81d877169eaec51cf3d0ba1f182550ec42eef6940480d3b917a9c; gdxidpyhxdE=JHmKI5nDXIIMEuO0fxvVnhkcLa6fcsRMahuziDikxPo5%2F733Ezwn7T9%2BdpoburB22HebOsqXdkv8hy2KEQl%2Flxe3spzXUYRcdo6%5CtXtPqWNTbxP3YguvBqZjlyWNqHay73W3WonDYDcvhTD3mt%2BfUXCsU5%5Co7WWALcdES5Kh1mvPby6m%3A1757002502148; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1756882276,1756959384,1756963700,1756964310; captcha_ticket_v2=2|1:0|10:1757002250|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfU3FlcnRVZDR3bEUyQl9yZUFtbHpqSUpaSnE0VXQ0ZUFIcnVFZmN5RmdDS1EyQTBxQUxXWVp5dlhXRGh3dDRFUipsODA1ZXlib2RzY3JaMmRfcUpXX194ZTFlV3FEclJ5WF84ZGZNellOZE4wM2tIOHFab3prclp2MVFtTzJzR1dPUXFYTERza3lyYTVoRjVmZWxLR2FWMGo0UHZ2OGVhZ3dac0pGM212cVBaLndiVGFmZ0R0ZnJhUlN5YVRFM1ltbWt5SlZHNW5nX0VNWkJTWk4xVWpucjVKQWJ5TWp3bC5rb3J6anJxYUsybDYzRzMzc1BWZU8xVTRfUWtZRWlVcTQzdFlPc2ZhY28qTEZ0bC4qZUpjUTBBSCpoVXdCLmc0VGZ6RVhuZG5zMnFpQVZadU8uZC54SHJGOVFUSWwqSEczckhXQ2hxMXlxSW02bFFDWjBtYlpIekRhLnF3U1BHSG9OZVBUXzVJQlEqTmxIZ2JmeEpyd3RTMC5LdWU2T0ZSNUhjTUJmcm81bWZGY1R2R0JqRUR1SkdVWVBOWEpZWmIxbVJqWXA2UE1sVXdrQmpvZGFoZSpJRG9BeCpwMEptVXVCZTJNV0xBdUx6d1JCSHVjV2lyNGZRTHNSYVE0OUpnYS4xZGNYeno5QWE2NWpFX0ouY0VpazBfTip6Z2VhYkYyQjlmQmc3N192X2lfMSJ9|5cadcc8971728c948d222e4fae2b43e83b88afc8e93277c57eb89b11de505896; q_c1=241810b593fe4164aa00417f16bc0886|1756881840000|1756881840000; __snaker__id=FiozAkmoxt16tmDH; BEC=4589376d83fd47c9203681b16177ae43; SESSIONID=fmclU7G2EneAakT1AX6uD3dYhgO55MhyZMfEPVQbmXX; JOID=VF8UAU7rys1e_9q3IpRYmUMeqkw_jKGtNans9hOtpa4cmbLiFWl4cDL93bImr8FG8MQy3zVv7C4PnyCi_Me85Rc=; osd=U14VC0_sy8xU_t22I55ZnkIfoE04jaCnNK7t9xmsoq8dk7PlFGhycTX83LgnqMBH-sU13jRl7SkOniqj-8a97xY=; DATE=1756197343036; cmci9xde=U2FsdGVkX18r4fUyNaOE8YANeJqyoClV8gg2gOFSlBDBGpMTdCxnlFKeboezanOVb7ZG69mybNutE8G1W9ceGg==; pmck9xge=U2FsdGVkX19Xel+UrAUolY17p7gbCutXbx3zYXP6KOI=; crystal=U2FsdGVkX18/bF5wL09zwthl4lvz2AAv7bPTlJkhZ2yG17n8fUeBNOwXS5K/p/W5441mAinhJsXuc20SVNE1rAFPx2GlmPuz0KOSCHYwnhW0WZjEg9ESnEE9V/pkFWGzPinrADIhaDzSPN33SoAFLhGrcTGafy4NqTYzK9iDo07ETFIStlOHnjH7pqXm2y2qqcnpPQyPftatR1qU6Y4fSFblm2OW0D/9FFS4YImMPt8PVGRVY5+dBmS2DHO2Z34i; vmce9xdq=U2FsdGVkX1+UA+fzUSAB0qjDnakH9TDBlIm5py9Vo+fo+BUTX7elxPa77Iz8MySW/3Ql0PGrrql1ZIwUKyvMgBJM1uVVbyQqjlp8mq5SWZhsTWGmkI5fiv37yJFG3d82KSNhj0DoRNhalWIGTmBFW6ym6LT+uXrXlQuc8VeyYFA=; assva6=U2FsdGVkX19tELItzDY1BCkP3Uni+D1yJA1VaSgW8rs=; assva5=U2FsdGVkX19h1vDUQymdJOmTL41112o4l6qa6IevMuPGXMhgKqB+9TR3I1umkGXjlbAaRgPoSDRMJn5QyBSyjg==; z_c0=2|1:0|10:1757002250|4:z_c0|92:Mi4xWDZMOFhRQUFBQUQ3b0JNdmRwajRHaVlBQUFCZ0FsVk5DZ2luYVFCaGd2OGlIaFRHaTZpZ0loc2x0RjU0ZmFZd3FB|7a06137528764841585d29ae3f5b5a5aea853a70519f880881003e34d2a62b40; tst=r'})

#打开首页知乎
driver.get("http://www.zhihu.com")

search_box = driver.find_element(By.XPATH,'//*[@id="Popover1-toggle"]')

#搜索框中输入
search_box.send_keys("python异常处理语句")

#模拟按下回车键
search_box.send_keys(Keys.ENTER)

#开始获取前面几页的资料：和链接

driver.implicitly_wait(3)

time.sleep(2)


for i in range(2, 10): #                         #//*[@id="SearchMain"]/div/div/div/div[3]/div/div/div/h2/span/div/div/a/span
    try:
        title = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[2]/div[3]/div/div/div/div[{num}]/div/div/div/h2/span/div/div/a/span'.format(num=i))
                                               #//*[@id="SearchMain"]/div/div/div/div[3]/div/div/div/h2/span/div/div/div/a/span
                                               #//*[@id="SearchMain"]/div/div/div/div[4]/div/div/div/h2/span/div/div/div/a/span
        link = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[2]/div[3]/div/div/div/div[{num}]/div/div/div/h2/span/div/div/a'.format(num=i))
        link = link.get_attribute('href')
        message = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div/div[2]/div[3]/div/div/div/div[{num}]/div/div/div/div/span/div/div/span/span[1]'.format(num=i))
    except NoSuchElementException as e:
        print("jump and continue !")
        print(e)
        continue

    data = {"标题": title.text,
            "介绍：": message.text,
            "链接": link
            }
    result_list.append(data)


pprint.pprint(result_list)
parent = psutil.Process(chrome_process.pid)
# for child in parent.children(recursive=True):
#     child.kill()
# parent.kill()

