import pandas as pd
import numpy as np
import requests
from lxml import etree
import re, time, random, datetime, os
from queue import Queue
import threading

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
    s.get(url=url_base, headers=headers, proxies=proxies)

    def __init__(self):
        self.title_list = []
        self.url_list = []
        self.info_list = []
        self.url_queue = Queue()

    def parser(self, url):
        res = self.s.get(url=url, headers=self.headers, proxies=self.proxies, verify=False)
        res_html = etree.HTML(res.text)
        goods_content = res_html.xpath("//li[@class='zg-item-immersion']")
        for each in goods_content:
            try:
                goods_href = each.xpath(".//a[@class='a-link-normal']/@href")[0]
                goods_title = each.xpath(".//div[@class='p13n-sc-truncated']/text()")[0]
                rank = each.xpath(".//span[@class='zg-badge-text']")[0]
                ASIN = re.search('dp/(.*)/', goods_href).group().split("/")[1]
                pic_url = each.xpath(".//div[@class='a-section a-spacing-small']/img/@src")[0]
                price = each.xpath(".//span[@class='p13n-sc-price']")[0]
                view_count = each.xpath(".//a[@class='a-size-small a-link-normal']/text()")[0]

                self.info_list.append((goods_href, goods_title, rank, ASIN, price, view_count))
                # self.get_pic(ASIN=ASIN, pic_url=pic_url)

            except Exception as e:
                print(e)


    # def get_pic(self, ASIN, pic_url,title=''):
    #     res_pic = self.s.get(pic_url, headers=self.headers, proxies=self.proxies, verify=False)
    #     file_path = 'data/pic/' + title + "/"
    #     if not os.path.exists(file_path):
    #         os.makedirs(file_path)
    #     file_name = 'data/pic/' + title + ASIN + '.png'
    #     with open(file_name, "wb") as f:
    #         f.write(res_pic.content)


if __name__ == '__main__':


    data = r"home and kitchen三级类目.xlsx"
    goods_data = pd.read_excel(data, encoding='utf-8', sheet_name='sheet1')

    best_seller = ABS()


    for each_url, each_count in zip(goods_data['ASIN'][70:], goods_data['评价数量'][70:]):
        best_seller.parser(url=url)

        time.sleep(1.5)
        while True:
            if not best_seller.url_queue.empty():
                try:
                    url = best_seller.url_queue.get()
                    zero_t = threading.Thread(target=best_seller.get_review, args=(url,))
                    zero_t.start()
                except:
                    print("请求链接出错，重试中...")
                    pass
                time.sleep(random.random())
            if best_seller.url_queue.empty():
                break
    view_goods_pd = pd.DataFrame(best_seller.view_list, columns=['review_goods', 'review_name', 'review_star', 'review_title',
                                                            'review_date', 'review_colour', 'review_size', 'review_body',
                                                            'review_useful'])
    aft = datetime.datetime.now().strftime('%m%d%H%M')
    file_name = 'data/goods_review/'+ "reviews-" + aft + ".xlsx"
    view_goods_pd.to_excel(file_name, encoding='utf-8')
    print(len(best_seller.view_list))
