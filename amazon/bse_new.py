import pandas as pd
import numpy as np
import requests
from lxml import etree
import re, time, random, datetime, os
from queue import Queue
import threading
import sys

class ABS:

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    }

    proxies = {
        "http": "http://49.86.181.43:9999",
    }

    url_base = "https://www.amazon.com"
    s = requests.Session()
    s.get(url=url_base, headers=headers)

    def __init__(self):
        # self.title_list = []
        # self.url_list = []
        self.info_list = []
        self.url_queue = Queue()

    def parser(self, sub_url, cat_title, sub_title):
        res = self.s.get(url=sub_url, headers=self.headers, proxies=self.proxies)
        res_html = etree.HTML(res.text)
        # categpry = res_html.xpath("//span[@class='category']/text()")[0]
        goods_content = res_html.xpath("//li[@class='zg-item-immersion']")
        for each in goods_content:
            try:
                goods_href = each.xpath(".//a[@class='a-link-normal']/@href")[0]
                goods_href = "https://www.amazon.com" + goods_href
                ASIN = re.search('dp/(.*)/', goods_href).group().split("/")[1]
            except:
                goods_href = None
                ASIN = None
            try:
                goods_title = each.xpath(".//a[@class='a-link-normal']/div/text()")[0].strip()
            except:
                goods_title = None
            rank = each.xpath(".//span[@class='zg-badge-text']/text()")[0]

            try:
                stars = each.xpath(".//span[@class='a-icon-alt']/text()")[0]
                stars = stars.split()[0]
            except:
                stars = None

            try:
                price = each.xpath(".//span[@class='p13n-sc-price']/text()")[0]
            except:
                price = None

            try:
                view_count = each.xpath(".//a[@class='a-size-small a-link-normal']/text()")[0]
            except:
                view_count= '0'

            self.info_list.append((cat_title, sub_title, sub_url, goods_title, goods_href, rank, ASIN, price, view_count, stars))
            print(self.info_list[-1])

def main():

    data = r"data/category/Best-Sellers-Home-Kitchen-06061053.xlsx"
    goods_data = pd.read_excel(data, encoding='utf-8')
    best_seller = ABS()

    for sub_url, cat_title, sub_title in zip(goods_data['sub_url'], goods_data['cat_title'],
                                             goods_data['sub_title']):
        best_seller.url_queue.put((sub_url, cat_title, sub_title))

    while True:
        try:
            thread_list = [threading.Thread(target=best_seller.parser, args=(best_seller.url_queue.get()))
                           for i in range(30) if best_seller.url_queue.empty()]
            for each in thread_list:
                print(each)
                each.start()
            for each in thread_list:
                each.join()
        except Exception as e :
            print(e)
            print("请求链接出错，重试中...")

        time.sleep(random.random())
        if best_seller.url_queue.empty():
            break

    view_goods_pd = pd.DataFrame(best_seller.info_list,
                                 columns=['cat_title', 'sub_title', 'sub_url', 'goods_title', 'goods_href', 'rank', 'ASIN', 'price', 'view_count','stars'])
    aft = datetime.datetime.now().strftime('%m%d%H%M')
    file_name = 'data/ABS/' + "best_seller" + aft + ".xlsx"
    view_goods_pd.to_excel(file_name, encoding='utf-8')
    print("output:",len(best_seller.info_list))

if __name__ == '__main__':
    main()