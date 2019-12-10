import numpy as np
import pandas as pd
import requests, lxml
from lxml import etree
import re, time, random, datetime


def weight_handle(weight):
    # 把kg g 都转化为数字存储
    if re.search("kg", weight.lower()):
        weight_int = float(weight.split(' ')[0]) * 1000
    else:
        weight_int = float(weight.split(' ')[0])

    return weight_int


def feature_handle(feature):
    import re
    patt = re.compile('(\d+)[^\d+]*[by\*x]\s*(\d+)')
    res = re.search(patt, feature.lower()).groups()
    return res

class GoodDetail:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    }

    proxies = {
        "http": "http://114.239.3.156:9999",
    }

    url_base = "https://www.amazon.com"
    s = requests.Session()
    s.get(url=url_base, headers=headers)

    def __init__(self):
        self.detail_list = []

    def get_detail(self, url):
        import re
        res = self.s.get(url, headers=self.headers)
        if str(res.status_code) == '200':
            res_html = etree.HTML(res.text)
        else:
            print("请求出错，状态码为：%s" % res.status_code)
            print(res.text)
            return
        # print(res.text)
        # res_html = etree.HTML(res.text)
        from bs4 import BeautifulSoup
        soup_res = BeautifulSoup(res.text, features="lxml")
        detail_text = soup_res.select('body')
        res_html = etree.HTML(str(detail_text[0]))

        # 类别
        kinds = res_html.xpath("//div[@class='twisterTextDiv text']/span[@class='a-size-base' and 1]/text()")[:]

        if not kinds:
            kinds = res_html.xpath('//div[@class="a-section a-spacing-none twisterShelf_displaySection"]/span/text()')[:]
        # 不同类别的编号
        sorts_codes = res_html.xpath('//li[starts-with(@id, "size_name")]/@data-defaultasin')[:]

        try:
            choosen_kinds = res_html.xpath(
                '//div[starts-with(@id, "variation")]/div/span/text()')
            if choosen_kinds:
                choose_kind = choosen_kinds[0].strip()
            else:
                choose_kind = res_html.xpath('//span[@class="shelf-label-variant-name"]/text()')[0].strip()
        except:
            choose_kind = "Just One Kind"

        item = {}
        if res_html.xpath('//div[@id="detail-bullets"]//div[@class="content"]/ul/li'):
            print("model-0")
            for each in res_html.xpath('//div[@id="detail-bullets"]//div[@class="content"]/ul/li'):
                li = each.xpath('string(.)')
                li = li.replace('\n', '').replace('\t', '')
                key = li.split(":")[0].strip()
                value = li.split(":")[1].strip()
                import re
                if not (re.search('rank', key.lower()) or re.search('review', key.lower())):
                    item[key] = value
            goods_rank = res_html.xpath('string(//li[@id="SalesRank"])')
            item['raw_goods_rank'] = goods_rank

        if res_html.xpath("//div[@id='detailBullets_feature_div']/ul"):
            absr = res_html.xpath('string(//div[@id="dpx-amazon-sales-rank_feature_div"]/li)')
            item['Amazon Best Sellers Rank'] = absr
            print("model-1")
            for each in res_html.xpath('//div[@id="detailBullets_feature_div"]/ul/li'):
                key = each.xpath('.//span/span[1]/text()')
                # print(key)
                value = each.xpath('.//span/span[2]/text()')
                # print(value)
                if key and value:
                    key = key[0].replace("\n", '').replace("\t", '').strip(": (")
                    value = value[0].replace("\n", '').replace("\t", '').strip(": (")
                    print(key, "---", value)
                    if key != "Customer Reviews":
                        item[key] = value

        if res_html.xpath("//div[@class='a-section table-padding']/table//tr"):
            print("model-2")
            for each in res_html.xpath("//div[@class='a-section table-padding']/table//tr"):
                key = each.xpath("string(.//th)")[:]
                # print(key, "---")
                value = each.xpath("string(.//td)")[:]
                #     print(key, value)
                if key and value:
                    key = key.replace("\n", '').replace("\t", '').strip()
                    value = value.replace("\n", '').replace("\t", '').strip()
                    if key != "Customer Reviews":
                        item[key] = value

        if res_html.xpath("//table[@id='productDetails_detailBullets_sections1']"):
            print("model-3")
            for each in res_html.xpath("//table[@id='productDetails_detailBullets_sections1']//tr"):
                # print("model1--in")
                key = each.xpath("string(./th)")[:]
                # print(key, "---")
                value = each.xpath("string(./td)")[:]
                # print(key, value)
                if key and value:
                    key = key.replace("\n", '').replace("\t", '').strip()
                    value = value.replace("\n", '').replace("\t", '').strip()
                    if key != "Customer Reviews":
                        item[key] = value


        if res_html.xpath("//table[@id='productDetails_techSpec_section_1']"):
            print("model-4")
            for each in res_html.xpath("//table[@id='productDetails_techSpec_section_1']//tr"):
                key = each.xpath("string(.//th)")[:]
                # print(key, "---")
                value = each.xpath("string(.//td)")[:]
                # print(key, value)
                if key and value:
                    key = key.replace("\n", '').replace("\t", '').strip()
                    value = value.replace("\n", '').replace("\t", '').strip()
                    if key != "Customer Reviews":
                        item[key] = value

        if res_html.xpath("//div[@class='wrapper USlocale']"):
            print("model-5")
            for each in res_html.xpath("////div[@class='wrapper USlocale']//tr"):
                # print("model3--in")
                key = each.xpath("string(.//td[@class='label'])")[:]
                # print(key, "---")
                value = each.xpath("string(.//td[@class='value'])")[:]
                # print(key, "---", value)
                if key and value:
                    key = key.replace("\n", '').replace("\t", '').strip()
                    value = value.replace("\n", '').replace("\t", '').strip()
                    if key != "Customer Reviews":
                        item[key] = value
                        print(key,"---", value)

        # 图片路径
        try:
            goods_pic_url = res_html.xpath('//img[@id="landingImage"]/@src')[0]
        except:
            goods_pic_url = None

        ASIN = item.get('ASIN', None)
        product_dimensions = item.get('Product Dimensions', None)
        package_dimensions = item.get('Package Dimensions', None)
        # if not product_dimensions:
        #     package_dimensions = item.get('Package Dimensions', None)
        product_weight = item.get('Item Weight', None)
        ship_weight = item.get('Shipping Weight', None)
        # ship_weight = item.get('Shipping Weight	', None)


        import re
        weight_str = re.compile(r'\(.*\)')
        if ship_weight:
            ship_weight = re.sub(weight_str,'', "".join(ship_weight))

        feature_list = res_html.xpath("//div[@id='feature-bullets']/ul/li/span/text()")
        features = []
        for feature in feature_list:
            feature = feature.strip()
            features.append(feature)

        goods_ranks = item.get('raw_goods_rank', None)
        goods_each_ranks = goods_ranks
        print(goods_ranks)
        if not goods_ranks:
            goods_ranks = item.get('Best Sellers Rank', None)
            if not goods_ranks:
                    goods_ranks = item.get('Amazon Best Sellers Rank', None)

        if goods_ranks:
            print("---")
            import re
            goods_rank = goods_ranks.replace("\n", '').replace("\t", '').replace("\xa0", ' ')
            patt = re.compile(r'[\(\{].*[\)\}]')
            patt2 = re.compile(r'\s{2,}')
            goods_rank = re.sub(patt, '', goods_rank)
            goods_rank = re.sub(patt2, ' ', goods_rank)
            goods_each_ranks = []

            for each in goods_rank.split('#')[1:]:
                goods_rank_num, goods_rank_sort = each.split("in", 1)
                goods_rank_sort = re.sub(weight_str, '', goods_rank_sort)
                goods_each_ranks.append((goods_rank_num.strip(), goods_rank_sort.strip()))
                print(goods_each_ranks)


        # 评价数量
        try:
            goods_view_count = res_html.xpath('//div[@id="averageCustomerReviews"]//span[@id="acrCustomerReviewText"]/text()')[0]
            goods_view_count = int(goods_view_count.split(" ")[0].replace(",", ""))
        except:
            goods_view_count = 0

        # 评价星级
        try:

            goods_view_star = res_html.xpath('//div[@id="averageCustomerReviews"]//span[@class="a-icon-alt"]/text()')[0]
            goods_view_star = float(goods_view_star.split(" ")[0])
        except:
            goods_view_star = None

        # 价格
        try:
            goods_price = res_html.xpath('//span[@id="priceblock_ourprice"]/text()')[0]

        except:
            goods_price = None

        if not goods_price:
            try:
                goods_price = res_html.xpath('//span[@id="priceblock_pospromoprice"]/text()')[0]
            except:
                goods_price = None

        # 品牌以及库存
        import json
        try:
            brand = res_html.xpath('//a[@id="bylineInfo"]/text()')[0]
        except:
            brand = None
        try:
            buy_box_info =  res_html.xpath('//*[@id="turboState"]/script/text()')[0]
            buy_box_json = json.loads(buy_box_info)
            stockOnHand = buy_box_json['eligibility']['stockOnHand']
        except:
            stockOnHand = None

        # 卖方
        try:
            seller = res_html.xpath('string(//div[@id="merchant-info"])')
            seller = seller.replace("\n", "").split(".")[0].strip()
            if not seller:
                try:
                    seller = res_html.xpath('string(//span[@id="merchant-info"])')
                    seller = seller.replace("\n", "").split(".")[0].strip()
                except:
                    seller = None
        except:
            seller = None


        each_detail_list = (goods_pic_url, ASIN, brand, goods_price, choose_kind, seller, stockOnHand, goods_view_count,product_dimensions,package_dimensions, product_weight, ship_weight,
                            goods_view_star, goods_each_ranks, sorts_codes,)

        self.detail_list.append(each_detail_list)


def pic_save(base_code, ASIN):

        import base64
        img_data = base64.b64decode(base_code)
        file = open(r"data/pic/" + str(ASIN)+'.jpg', 'wb')
        file.write(img_data)
        file.close()

if __name__ == '__main__':

    data_path = r'E:\模拟开发\筛选开发模拟\\'
    # data_file = data_path + r"\ABS\ABS_BathBombs.xlsx"
    data_file = r'data/goods_rank_list/baby Apron-05301754.csv'
    data = pd.read_csv(data_file)
    # data.columns = ['#', 'title', 'brand', 'price', 'category', 'rank', 'sales', 'income', 'reviews', 'stars', 'seller',
    #                 'scounts', 'ASIN', 'gurl']
    goods_detail = GoodDetail()
    for url in data['goods_url_full']:
        if url:
            print(url)
            goods_detail.get_detail(url)
            time.sleep(random.random())

    details_pd = pd.DataFrame(goods_detail.detail_list,
                              columns=['goods_pic_url', 'ASIN', 'brand', 'goods_price', 'choose_kind','seller','stockOnHand', 'goods_view_count',
                                       'product_dimensions', 'package_dimensions','product_weight', 'ship_weight',
                                       'goods_view_star','goods_each_ranks',
                                       'sorts_codes'])
    #
    aft = datetime.datetime.now().strftime('%m%d%H%M')
    # file_name = "data/goods_detail/" + aft + ".xlsx"
    # details_pd.to_excel(file_name, encoding='utf-8')

    for base_code_full, ASIN in zip(details_pd['goods_pic_url'], details_pd['ASIN']):
        base_code = base_code_full.split(',')[1]
        pic_save(base_code, ASIN)

    time.sleep(3)
    details_pd['pic_url'] = "E:\爬虫pycharm\data\pic\\" +  details_pd['ASIN'] + ".jpg"
    details_pd['pic_table_url'] = '<table> <img src=' + '\"' +details_pd['pic_url'] + '\"' +'height="120" >'
    file_name_new = "data/goods_detail/" + aft + "_without_ad.xlsx"
    details_pd.to_excel(file_name_new,  encoding='utf-8')