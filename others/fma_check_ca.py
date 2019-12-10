import pandas as pd
import requests
from lxml import etree
import re, time, random, datetime
import pymysql
import os
import urllib
from aip import AipOcr

APP_ID = '11240997'
API_KEY = '6ZU9O51SKfbaZyg0vzAUWXqN'
SECRET_KEY = 'xtCepeZVrdZ6LSHBDf0xNhYq7PEdY8No '
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)

# User_Agent 库 随机选取作为请求头
head_user_agent = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def seller_handle(seller):
    """
    卖家处理 识别为AMZ/FMA/FBM
    :param seller: 卖家字段
    :return:
    """
    if not seller:
        return None
    else:
        if re.search('sold by Amazon.com', seller, re.I):
            return 'AMZ'
        elif re.search('Fulfilled by Amazon', seller, re.I):
            return 'FBA'
        else:
            return 'FBM'

# 定义一个获取详情页的类
class GoodDetail:
    # headers = {
    #     # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:67.0) Gecko/20100101 Firefox/67.0"
    # }
    # 加拿大 初次请求 用来保存请求状态
    url_base = "https://www.amazon.ca"
    s = requests.Session()
    row_headers = {
        'User-Agent': random.choice(head_user_agent),
        "Host": "www.amazon.ca",
        "Upgrade-Insecure-Requests": "1",
    }
    s.headers.update(row_headers)
    # 在初次请求后修改请求头
    res_row = s.get(url=url_base)
    s.headers.update({
        "Host": "www.amazon.ca",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",  # 是否通过键盘鼠标操作得到的链接 是
        "Upgrade-Insecure-Requests": "1",
    })
    res_row_html = etree.HTML(res_row.text)
    title = res_row_html.xpath("//title/text()")[0]
    print(title)
    # 初次请求的机器人识别 ：如果返回的数据是机器人检测的页面 识别到指定的验证码图片，人工识别后输入
    if title == 'Robot Check':
        img_src = res_row_html.xpath("//div[@class='a-row a-text-center']/img/@src")[0]
        print("验证码图片链接：", img_src)
        res_pic = s.get(img_src).content
        amzn_code = res_row_html.xpath("//input[@name='amzn']")[0].get('value')
        amzn_r_code = res_row_html.xpath("//input[@name='amzn-r']")[0].get('value')
        ocr_options = {}
        ocr_options["detect_direction"] = "true"
        ocr_options["probability"] = "true"
        ocr_options["language_type"] = "ENG"
        ocr_json = client.basicAccurate(res_pic, ocr_options)
        print(ocr_json)
        if ocr_json.get('words_result_num', None) == 1:
            ocr_result = ocr_json.get('words_result')[0].get('words')
            print('机器人检测OCR结果为', ocr_result)
        else:
            ocr_result = input("输入验证码：")
            print('机器人检测OCR结果为', ocr_result)
        captcha_row_url = "https://www.amazon.ca/errors/validateCaptcha?"
        captcha_url = captcha_row_url + "&amzn=" + amzn_code + "&amzn-r=" + amzn_r_code + "&field-keywords=" + \
                      ocr_result
        ocr_headers = {
            "Host": "www.amazon.ca",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
        }
        s.get(captcha_url, headers=ocr_headers)
    print("状态cookies：", s.cookies.items())

    def __init__(self):
        # 初始化一些用来存储信息的列表
        self.detail_list = []
        self.rank_list = []
        self.sec_list = []
        self.begin = 0  # 请求出错计数
        self.begin_503 = 0  # 503请求出错计数
        self.error_list = []  # 未能正确请求的链接 再所有请求结束后 会再次请求（再尝试一次 不会循环）

    def get_detail(self, url):
        import re

        if re.search('slredirect', url):
            ad_plus = 1
            ad_headers = {
                "User-Agent": random.choice(head_user_agent),
                "Host": "www.amazon.ca",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-User": "?1",   # 是否通过键盘鼠标操作操作发出请求
                "Upgrade-Insecure-Requests": "1",
            }
            try:
                url = "https://www.amazon.ca" + urllib.parse.unquote(url.split('url=')[1].split("ref")[0])
            except:
                pass
            print(url)
            res = self.s.get(url, headers=ad_headers, timeout=20)
        else:
            ad_plus = 0
            try:
                url = url.split('/ref')[0]
            except:
                pass
            print(url)
            res = self.s.get(url, timeout=20)

        print(self.s.headers)
        print(res.headers)
        res_row_html = etree.HTML(res.text)
        title = res_row_html.xpath("//title/text()")[0]
        print(res.status_code)
        print(title)
        # 请求过程中的机器人识别
        if title == 'Robot Check':
            img_src = res_row_html.xpath("//div[@class='a-row a-text-center']/img/@src")[0]
            print("验证码图片链接：", img_src)
            amzn_code = res_row_html.xpath("//input[@name='amzn']")[0].get('value')
            amzn_r_code = res_row_html.xpath("//input[@name='amzn-r']")[0].get('value')
            ocr_result = input("输入验证码：")
            print('机器人检测OCR结果为', ocr_result)
            captcha_row_url = "https://www.amazon.ca/errors/validateCaptcha?"
            captcha_url = captcha_row_url + "&amzn=" + amzn_code + "&amzn-r=" + amzn_r_code + "&field-keywords=" + \
                          ocr_result
            self.s.get(captcha_url)
            print("状态cookies：", self.s.cookies.items())

        #  如果是广告链接，且未能正确跳转 返回302的再次尝试
        if res.status_code == 302:
            real_url = res.headers.get('location', '')
            print("跳转到真实链接：", real_url)
            self.get_detail(url=real_url)

        #  返回503， 调整请求头 更换UA后再次尝试
        if res.status_code == 503:

            time.sleep(random.uniform(2, 5))
            print("try again because 503")
            self.begin_503 += 1
            if self.begin_503 >= 3:
                print('该链接{}因503跳转访问出错次数超过3次, 请手动尝试添加'.format(url))
                if url not in self.error_list:
                    self.error_list.append(url)
                return
            headers_503 = {
                "User-Agent": random.choice(head_user_agent),
                "Host": "www.amazon.ca",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-User": "?1",
                "Upgrade-Insecure-Requests": "1",
            }
            self.s.headers.update(headers_503)
            self.get_detail(url=url)
        if res.status_code != 200:
            print("页面错误，状态码为：", res.status_code)
            print(res.text)
            try:
                print(etree.HTML(res.text).xpath("//title/text()")[0])
            except:
                pass
            return

        from bs4 import BeautifulSoup
        soup_res = BeautifulSoup(res.text, features='lxml')
        detail_text = soup_res.select('body')
        res_html = etree.HTML(str(detail_text[0]))

        try:
            goods_title = res_html.xpath("string(//span[@id='productTitle'])")
            goods_title = goods_title.replace("\n", '').replace('\t', '').strip()
        except:
            goods_title = None

        if not goods_title:
            time.sleep(random.uniform(2, 5))
            print("try again")
            self.begin += 1
            if self.begin >= 3:
                print('该链接{}访问出错次数超过3次, 请手动尝试添加'.format(url),"可能是不可解析的广告链接")
                return
            self.get_detail(url=url)

        self.begin = 0
        # 不同类别、颜色、款式的编号
        # 仅仅能获取到部分可以直接点击得到的ASIN, 如果需要完整的父子ASIN数据可使用 keepa API
        try:
            sorts_codes = res_html.xpath('//*[starts-with(@id, "size_name")]/@data-defaultasin')[:]
            color_sorts = res_html.xpath('//*[starts-with(@id, "color_name")]/@data-defaultasin')[:]
            style_sorts = res_html.xpath('//*[starts-with(@id, "style_name")]/@data-defaultasin')[:]
            sort_list_raw = sorts_codes + color_sorts + style_sorts
            sort_list = list(set(sort_list_raw))

            if "" in sort_list:
                sort_list.remove('')

            sorts_color_url = res_html.xpath("//*[starts-with(@id, 'color_name')]/@data-dp-url")[:]
            sorts_size_url = res_html.xpath("//*[starts-with(@id, 'size_name')]/@data-dp-url")[:]
            sorts_style_url = res_html.xpath("//*[starts-with(@id, 'style_name')]/@data-dp-url")[:]
            asin_patt = re.compile("dp/(.*)/")
            sort_url_raw = sorts_color_url + sorts_size_url + sorts_style_url
            print("sort_list_raw:", sort_list_raw)
            print("sort_url_raw:", sort_url_raw)

            sort_url_list = [re.search(asin_patt, each).groups()[0] for each in sort_url_raw if each]
            sort_url_list = list(set(sort_url_list))
            if '' in sort_url_list:
                sort_url_list.remove('')
            sort_list.extend(sort_url_list)
        except:
            sort_list = []

        item = {}
        if res_html.xpath('//div[@id="detail-bullets"]//div[@class="content"]/ul/li'):
            print("model-0")
            for each in res_html.xpath('//div[@id="detail-bullets"]//div[@class="content"]/ul/li'):
                li = each.xpath('string(.)')
                li = li.replace('\n', '').replace('\t', '')
                try:
                    key = li.split(":")[0].strip()
                    value = li.split(":")[1].strip()
                except:
                    key = 'miss key'
                    value = 'miss value'
                import re
                if not (re.search('rank', key.lower()) or re.search('review', key.lower())):
                    item[key] = value
            goods_rank = res_html.xpath('string(//li[@id="SalesRank"])')
            item['raw_goods_rank'] = goods_rank

        if res_html.xpath('//*[@id="productDetailsTable"]//div[@class="content"]/ul/li'):
            print("加拿大站-model-0")
            for each in res_html.xpath('//*[@id="productDetailsTable"]//div[@class="content"]/ul/li'):
                li = each.xpath('string(.)')
                li = li.replace('\n', '').replace('\t', '')
                try:
                    key = li.split(":")[0].strip()
                    value = li.split(":")[1].strip()
                except:
                    key = 'miss key'
                    value = 'miss value'
                import re
                if not (re.search('rank', key.lower()) or re.search('review', key.lower())):
                    item[key] = value
            goods_rank = res_html.xpath('string(//li[@id="SalesRank"])')
            item['raw_goods_rank'] = goods_rank

        if res_html.xpath("//div[@class='pdTab']"):
            print('加拿大站-model-1')
            for each in res_html.xpath("//div[@class='pdTab']//tr"):
                key = each.xpath("string(.//td[@class='label'])")
                # print(key, "---")
                value = each.xpath("string(.//td[@class='value'])")
                if key and value:
                    key = key.replace("\n", '').replace("\t", '').strip()
                    value = value.replace("\n", '').replace("\t", '').strip()
                    if key != "Customer Reviews":
                        item[key] = value
        if res_html.xpath("//div[@id='detailBullets_feature_div']/ul"):
            absr = res_html.xpath('string(//div[@id="dpx-amazon-sales-rank_feature_div"]/li)')
            item['Amazon Best Sellers Rank'] = absr
            print("model-1")
            for each in res_html.xpath('//div[@id="detailBullets_feature_div"]/ul/li'):
                key = each.xpath('.//span/span[1]/text()')
                value = each.xpath('.//span/span[2]/text()')
                if key and value:
                    key = key[0].replace("\n", '').replace("\t", '').strip(": (")
                    value = value[0].replace("\n", '').replace("\t", '').strip(": (")
                    print(key, "---", value)
                    if key != "Customer Reviews":
                        item[key] = value

        if res_html.xpath("//div[@class='a-section table-padding']/table//tr"):
            print("model-2")
            for each in res_html.xpath("//div[@class='a-section table-padding']/table//tr"):
                key = each.xpath("string(.//th)")
                value = each.xpath("string(.//td)")
                if key and value:
                    key = key.replace("\n", '').replace("\t", '').strip()
                    value = value.replace("\n", '').replace("\t", '').strip()
                    if key != "Customer Reviews":
                        item[key] = value

        if res_html.xpath("//table[@id='productDetails_detailBullets_sections1']"):
            print("model-3")
            for each in res_html.xpath("//table[@id='productDetails_detailBullets_sections1']//tr"):
                key = each.xpath("string(./th)")
                value = each.xpath("string(./td)")
                if key and value:
                    key = key.replace("\n", '').replace("\t", '').strip()
                    value = value.replace("\n", '').replace("\t", '').strip()
                    if key != "Customer Reviews":
                        item[key] = value

        if res_html.xpath("//table[@id='productDetails_techSpec_section_1']"):
            print("model-4")
            for each in res_html.xpath("//table[@id='productDetails_techSpec_section_1']//tr"):
                key = each.xpath("string(.//th)")
                value = each.xpath("string(.//td)")
                if key and value:
                    key = key.replace("\n", '').replace("\t", '').strip()
                    value = value.replace("\n", '').replace("\t", '').strip()
                    if key != "Customer Reviews":
                        item[key] = value

        if res_html.xpath("//div[@class='wrapper USlocale']"):
            print("model-5")
            for each in res_html.xpath("////div[@class='wrapper USlocale']//tr"):
                key = each.xpath("string(.//td[@class='label'])")
                value = each.xpath("string(.//td[@class='value'])")
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

        asin = item.get('ASIN', None)

        try:
            sort_list.append(asin)
        except:
            pass
        multi_asin = list(set(sort_list))
        print("-----------")
        print(multi_asin)
        print("-----------")
        product_dimensions = item.get('Product Dimensions', None)
        package_dimensions = item.get('Package Dimensions', None)
        product_weight = item.get('Item Weight', None)
        date_on_shelf = item.get('Date first listed on Amazon', None)
        if not date_on_shelf:
            date_on_shelf = item.get('date_on_shelf', None)

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

        category_main = None
        rank_main = None
        if not goods_ranks:
            goods_each_ranks = {}
            self.rank_list.append(goods_each_ranks)

        if goods_ranks:
            print("---")
            import re
            weight_str = re.compile(r'\(.*\)')
            goods_rank = goods_ranks.replace("\n", '').replace("\t", '').replace("\xa0", ' ')
            patt = re.compile(r'[\(\{].*[\)\}]')
            patt2 = re.compile(r'\s{2,}')
            goods_rank = re.sub(patt, '', goods_rank)
            goods_rank = re.sub(patt2, ' ', goods_rank)
            goods_each_ranks = {}

            for each in goods_rank.split('#')[1:]:
                goods_rank_num, goods_rank_sort = each.split("in", 1)
                try:
                    goods_rank_num = int(goods_rank_num.replace(',','').strip())
                except:
                    pass
                goods_rank_sort = re.sub(weight_str, '', goods_rank_sort)
                goods_each_ranks[goods_rank_sort.strip()] = goods_rank_num

            self.rank_list.append(goods_each_ranks)
            print(self.rank_list[-1])

            try:
                category_main = list(self.rank_list[-1].keys())[0]
                rank_main = int(list(self.rank_list[-1].values())[0])
            except:
                category_main, rank_main = None, None
            # print(category_main, rank_main)
        # 评价数量
        try:
            goods_review_count = res_html.xpath('//div[@id="averageCustomerReviews"]//span[@id="acrCustomerReviewText"]/text()')[0]
            goods_review_count = int(goods_review_count.split(" ")[0].replace(",", ""))
        except:
            goods_review_count = 0

        # 评价星级
        try:

            goods_review_star = res_html.xpath('//div[@id="averageCustomerReviews"]//span[@class="a-icon-alt"]/text()')[0]
            goods_review_star = float(goods_review_star.split(" ")[0])
        except:
            goods_review_star = None

        try:
            goods_price = res_html.xpath("//span[starts-with(@id,'priceblock')]/text()")[0]
        except:
            goods_price =None

        try:
            brand = res_html.xpath('//a[@id="bylineInfo"]/text()')[0]
        except:
            brand = None

        # 卖方
        try:
            seller = res_html.xpath('string(//div[@id="merchant-info"])')
            seller = seller.replace("\n", "").split("Reviews")[0].strip()
            if not seller:
                try:
                    seller = res_html.xpath('string(//span[@id="merchant-info"])')
                    seller = seller.replace("\n", "").split("Reviews")[0].strip()
                except:
                    seller = None
        except:
            seller = None

        try:
            seller_cls = seller_handle(seller)
        except:
            seller_cls = None

        each_detail_list = (goods_pic_url,goods_title, asin, brand, ad_plus, goods_price, seller, seller_cls,
                            date_on_shelf, goods_review_count,product_dimensions, package_dimensions,
                            product_weight, goods_review_star, category_main,rank_main, goods_each_ranks)
        if goods_title:
            self.detail_list.append(each_detail_list)


def pic_save(base_code, asin):
    import base64
    img_data = base64.b64decode(base_code)
    if not os.path.exists("../data/pic/"):
        os.makedirs('../data/pic/')
    with open(r"../data/pic/" + str(asin) + '.jpg', 'wb') as f:
        f.write(img_data)


def main(data_file, start=0, end=61):
    goods_detail = GoodDetail()

    if data_file.endswith('csv'):
        data = pd.read_csv(data_file)
        # 选择数据范围
        # for url in data['goods_url_full'][起始位置:结束位置]
        for url in data['goods_url_full'][start: end]:
            if url:
                # print(url)
                try:
                    goods_detail.get_detail(url)
                except Exception as e:
                    print(e)
                time.sleep(random.random())

    if data_file.endswith('xlsx'):
        data = pd.read_excel(data_file, encoding='utf-8')
        for asin in data['asin'][start: end]:
            if asin:
                url = "https://www.amazon.ca/dp/" + str(asin)
                print(url)
                goods_detail.get_detail(url)
                time.sleep(random.random())

    last_info_list = goods_detail.detail_list

    # 判断是否有错误的页面，返回链接列表 再试一次
    another_list = None
    print("error_list:", goods_detail.error_list)
    if goods_detail.error_list:
        another_detail = GoodDetail()
        for each in goods_detail.error_list:
            another_detail.get_detail(each)
        another_list = another_detail.detail_list

    if another_list:
        last_info_list.extend(another_list)

    details_pd = pd.DataFrame(last_info_list,
                              columns=["goods_pic_url","goods_title", "asin", "brand", "ad_plus", "goods_price",
                                       "seller", "seller_cls", "date_on_shelf", "goods_review_count",
                                       "product_dimensions", "package_dimensions", "product_weight",
                                       "goods_review_star", "category_main","rank_main", "goods_each_ranks"])
    # ranks_pd = pd.DataFrame(goods_detail.rank_list)
    aft = datetime.datetime.now().strftime('%m%d%H%M')

    for base_code_full, asin in zip(details_pd['goods_pic_url'], details_pd['asin']):
        try:
            if base_code_full:
                base_code = base_code_full.split(',')[1]
                pic_save(base_code, asin)
        except:
            print("保存图片出错")

    time.sleep(3)

    # abs_path为项目的跟路径，相当于域
    abs_path = os.path.abspath('../')
    data_path = abs_path + "/data/goods_detail/"
    if not os.path.exists(data_path):
        os.makedirs(data_path)
    file_name = data_path + aft + "_with_ad.xlsx"

    details_pd['pic_url'] = abs_path + r"\data\pic\\" + details_pd['asin'] + ".jpg"
    details_pd['pic_table_url'] = '<table> <img src=' + '\"' + details_pd['pic_url'] + '\"' + 'height="140" >'
    # 获取 子类目列表 返回类似稀疏矩阵 进行数据连接
    # last_pd = pd.concat([details_pd, ranks_pd], axis=1)
    # 是否删除排名相同的行
    # details_pd.drop_duplicates(subset=['category_main', 'rank_main'], inplace=True)
    details_pd.to_excel(file_name, encoding='utf-8', engine='xlsxwriter')


if __name__ == '__main__':

    data_file = r"../data/category/Hanging Jewelry Organizers_1209_1654.xlsx"

    main(data_file, start=10, end=15)
