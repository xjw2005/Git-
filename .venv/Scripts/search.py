# -*- coding:utf-8 -*-
import requests  #发送请求
from Scripts.server import search
from bs4 import BeautifulSoup  #解析页面
import re
import pandas as pd
from time import sleep
import os
import random


#伪装浏览器请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:142.0) Gecko/20100101 Firefox/142.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "en-US,en;q=0.5",
    "Connection": "keep-alive",
    "Cookie": "_xsrf=6gr2Af9NZBGZT3jDUAstKY10otzam63Q; __zse_ck=004_ugsmQTMD1WaBhS9hoIbIJ8llldFKeDmgcKEvOkm8vAGIk79I8nwYvM1QCCdzPukou1We=glg=ijP3DdXhqxdwfH3q/YEYbGfN9hTDXXuda2oHGANam7xTih8ND4BNjg9-o6fLim/8de/Do/1AE0KjN1ug/gfhkPChQ9ZQdQQJBsJNII29D6mE5vIahdDY+WbuQWiTkFvNHa4uBqx0esf/flUIXSsHxgv75X19dcRX018O8aHO+Bqr6d/8X+wR6gY8; _zap=82dfae0b-2608-4bf9-8c16-810ad145de26; d_c0=-6ATL3aY-BqPTlm37W1YHtC2T9BkqkS9T_8=|1756139563; captcha_session_v2=2|1:0|10:1756804410|18:captcha_session_v2|88:dTY1WE5FcFFKU0crN29saVNQQnIvVnpPT0xROVZxSjVIVWsrQ1AvOEsrSU1kbnlmUlMrOEUxVkNXd1NHbVY5RA==|f09ae07342f213dce8706d2743b08ac7299263b1309cd14a33be4e5a198bdef7; gdxidpyhxdE=1lHt8%2B3B0cK8ylJtsJzXkAcu4MHONcoBCoQNwH%2BguZDdjmxPPMyCPzlZkCU%2FOqO2O%5CE4ugCw7kV5%2Fycet6ka2css8mTp5BIvOZXukDRjA13tN1fSLb522GSdNSb3hoEs6a2%2FYnIsPrnBdddcXGOUX%2ByVlDDTlKiD9RnwJ51XrQgq%2Fc4u%3A1756691906275; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1756733877,1756737668,1756804412,1756882276; captcha_ticket_v2=2|1:0|10:1756804420|17:captcha_ticket_v2|728:eyJ2YWxpZGF0ZSI6IkNOMzFfOGFvLjgqMWhnXzJKNHRYejFQR014c3lXaVRxdUpOWFFscENKZklFMHk1R1lkazl5YzlubmlVbFI5VEVzOC5ZWnA4TWJSKmx2bXpHbHd5VzQzbzE2LlU5ZkNVRWFYSzF1cG5BaUtFWktyWkZvQ19vZml6eWJ2UGMyOUhlcG1OKlNBRVdyS1BVQ0dDdGtlS2ZPdkRCVWRIZTU2dlBKaWprYVAzMEZYVVY1MjRmaWtvSVpEeC4waVdmRTNJaHFZc2dpTTVvazQyai5FSjBaclJ0SHhKajB3NUFyeGVjZENoVHZqR0gqWkQ4bUJ6WlFoMzF5aE9NODlkYWVadk5fcWwzcmptVDNrY1EqYUllQW9Id19Qb0JrMk1lMWZ4T2tJYVFpdHVYZHBqbWhJUjB1bGZVRWFFVFMqOVljcXVwUkp1TEJJNXJRKnAzY0lkc2JhdWF4RExrQVM2d3ZaVDFMejZZZTY2UUFlVktJWXlPd1dWOXNLS0YxNXhxeEk0RlBXdlhlVkQ2RXUqeG44ZHhQS2FtOVFaOFc1bzhIRUtmbWRpLkpzaTBLUUU2a25nRDNELncyTm5NOE5SYlVMakh2TXc0VEJzT2dIV0p5X3llV2p2eTlRbTYzU3FCKmR6QmY2RHQ5dVZTZmNQLmcxYjJKUTQ0MVZnUXFzY0xSWTVCUDhmcVFEbk1rclg3N192X2lfMSJ9|2b54fc3aeedc6fe2396a52649072069b37db75fa553e06868a5745d7a070f2c2; z_c0=2|1:0|10:1756881843|4:z_c0|92:Mi4xNWhMdFB3QUFBQUQ3b0JNdmRwajRHaVlBQUFCZ0FsVk5WQU9rYVFCQVZ2ZGJPTE5oalBjUll2OVloZVlyelRJOXZR|761b21c336710f05bda622fe04c91ce05f05ebb248ee6c394e4fcb68022745fb; q_c1=241810b593fe4164aa00417f16bc0886|1756881840000|1756881840000; SESSIONID=Fb75Hj0YpKmzSTU3mIinCuOAiCgmywrWd8LowhfOoP4; JOID=VlEcAUiCKz6AupkQTv-xYJNV6-NZyUkCtPX-IBz1bVPx6MpIfcxnjO6wlBtEQUqoNg3ytUgWmMVy29jFxzS-q70=; osd=UlsQC0qGITKKuJ0aQvWzZJlZ4eFdw0UItvH0LBb3aVn94shMd8Btjuq6mBFGRUCkPA_2v0QcmsF419LHwz6yob8=; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1756907346; HMACCOUNT=D5E1167644DFAE08; BEC=244e292b1eefcef20c9b81b1d9777823; tst=r",
    "x-zse-93": "101_3_3.0",
    "x-zse-96": "2.0_hgl4Bo=9A/11dJZkuutrrGIxknWheib9g4k94qy2qmrqdryspQna+dFJk9BqO1gu"
}


def search(v_keyword):
    """

    :param v_keyword:  关键字
    :return:  爬去结果
    """
    #获取每页的搜索结果
    print("开始搜索")
    wait_second = random.randint(1, 3)
    sleep(wait_second)
    url = "https://www.zhihu.com/search?q=" + v_keyword
    sleep(1)
    r = requests.get(url, headers=headers)
    fileName = v_keyword + ".html"
    soup = BeautifulSoup(r.text, "lxml")
    result_list = soup.select('.List > dive > dive')
    print(soup)

def test():
    print("开始搜索")
    wait_second = random.randint(1, 3)
    sleep(wait_second)
    url = "https://www.zhihu.com/api/v4/search_v3?gk_version=gz-gaokao&t=general&q=ax210&correction=1&offset=0&limit=20&filter_fields=&lc_idx=0&show_all_topics=0&search_source=Normal"
    sleep(1)
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "lxml")
    print(soup)


if __name__ == '__main__':
    # serach_keyword = input("搜索关键字")
    # search(serach_keyword)
    test()