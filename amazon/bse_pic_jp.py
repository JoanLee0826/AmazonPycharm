import pandas as pd
import requests
from lxml import etree
import re, time, random


class BSR():

    info_list = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
        (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    }

    proxies = {
        "http": "http://49.86.181.43:9999",
    }

    url_base = "https://www.amazon.co.jp"
    s = requests.Session()

    s.get(url=url_base, headers=headers)

    def parse(self, url):

        count = 1
        res = self.s.get(url=url, headers=self.headers)
        res_html = etree.HTML(res.text)
        try:
            category = res_html.xpath("//span[@class='category']/text()")[0]
        except:
            category = None
        if not category:
            count += 1
            print('try again')
            self.parse(url)

        goods_content = res_html.xpath("//div[@class='zg_itemRow']")
        for each in goods_content:
            try:
                rank_in = each.xpath(".//span[@class='zg_rankNumber']/text()")[0].strip(".")
            except:
                rank_in = None

            try:
                info_dict = each.xpath(".//div[@class='a-fixed-left-grid p13n-asin']/@data-p13n-asin-metadata")[0]
                print(info_dict)
                ASIN = dict(info_dict)['asin']
                print(ASIN)
            except:
                ASIN = None

            try:
                goods_review_count = int(each.xpath(".//a[@class='a-size-small a-link-normal']/text()")[0])
            except:
                goods_review_count = 0
            self.info_list.append((category, rank_in, ASIN, goods_review_count))
            #     # pic_url = each.xpath(".//div[@class='a-section a-spacing-small']/img/@src")[0]
            #
            #     # res_pic = s.get(pic_url, headers=headers, proxies=proxies, verify=False)
            #     # file_name = r'E:\爬虫pycharm\data\pic\\' + ASIN + '.png'
            #     with open(file_name, "wb") as f:
            #         f.write(res_pic.content)
            #         time.sleep(random.random())
            # except Exception as e:
            #     print(e)
    def run(self, row_url):

        for i in range(6, 7):
            url = row_url + '?pg=' + str(i)
            print(url)
            self.parse(url)
            time.sleep(random.uniform(1,3))

        aft = "_" + time.strftime("%m_%d_%H_%M", time.localtime())
        col = ['category', 'rank_in', 'ASIN', 'goods_review_count']
        data_pd = pd.DataFrame(self.info_list, columns=col)
        file_path = r'E:\爬虫pycharm\data\category\\'
        try:
            category = data_pd['category'][0]
        except:
            category = None
        print('{}类目下的{}条数据收集完毕'.format(category, len(data_pd)))
        data_pd.to_excel(file_path + category + aft + '.xlsx', encoding='utf-8',engine='xlsxwriter')

if __name__ == '__main__':

    bsr = BSR()
    url = 'https://www.amazon.com/gp/bestsellers/lawn-garden/3742271/'
    bsr.run(url)