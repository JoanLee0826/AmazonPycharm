import pandas as pd
import requests, lxml
from lxml import etree
import re, time, random, datetime
import threading, queue
import os
from aip import AipOcr


APP_ID = '11240997'
API_KEY = '6ZU9O51SKfbaZyg0vzAUWXqN'
SECRET_KEY = 'xtCepeZVrdZ6LSHBDf0xNhYq7PEdY8No '
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
url = 'https://www.amazon.com'

class GoodDetail:
    head_user_agent = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                       'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                       'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                       'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                       'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                       'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                       'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11']

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
        # "User-Agent": random.choice(head_user_agent)
    }

    proxies = {
        "http": "http://114.217.241.20:8118",
        "https:": "https://157.245.88.191:8080"
    }

    url_base = "https://www.amazon.com"

    s = requests.Session()
    s.headers.update({'User-Agent': random.choice(head_user_agent)})
    res = s.get(url=url_base, headers=headers, timeout=20)
    res_row_html = etree.HTML(res.text)
    title = res_row_html.xpath("//title/text()")[0]
    if title == 'Robot Check':
        img_src = res_row_html.xpath("//div[@class='a-row a-text-center']/img/@src")[0]
        print("验证码图片链接：", img_src)
        amzn_code = res_row_html.xpath("//input[@name='amzn']")[0].get('value')
        amzn_r_code = res_row_html.xpath("//input[@name='amzn-r']")[0].get('value')
        ocr_result = input("输入验证码：")
        # ocr_options = {}
        # ocr_options["detect_direction"] = "true"
        # ocr_options["probability"] = "true"
        # ocr_options["language_type"] = "ENG"
        # ocr_json = client.basicAccurate(img_src)
        # print(ocr_json)
        # if ocr_json.get('words_result_num', None) == 1:
            # ocr_result = ocr_json.get('words_result')[0].get('+words')
        print('机器人检测OCR结果为', ocr_result)
        captcha_row_url = "https://www.amazon.com/errors/validateCaptcha?"
        captcha_url = captcha_row_url + "&amzn=" + amzn_code + "&amzn-r=" + amzn_r_code + "&field-keywords=" + \
                      ocr_result
        s.get(captcha_url)
    print(s.headers.get('User-Agent'))

    def __init__(self):
        self.detail_list = []
        self.rank_list = []
        self.sec_list = []
        self.begin = 0
        self.url_queue = queue.Queue()
        self.undo_list = []

    def get_detail(self, url):
        import re
        if re.search('slredirect', url):
            ad_plus = 1
        else:
            ad_plus = 0
        self.s.headers.update({'User-Agent': random.choice(self.head_user_agent)})
        res = self.s.get(url, headers=self.headers, verify=False, proxies=self.proxies)
        res_row_html = etree.HTML(res.text)
        title = res_row_html.xpath("//title/text()")[0]
        print(title)
        if title == 'Robot Check':
            img_src = res_row_html.xpath("//div[@class='a-row a-text-center']/img/@src")[0]
            print("验证码图片链接：", img_src)
            amzn_code = res_row_html.xpath("//input[@name='amzn']")[0].get('value')
            amzn_r_code = res_row_html.xpath("//input[@name='amzn-r']")[0].get('value')
            ocr_result = input("输入验证码：")
            # ocr_options = {}
            # ocr_options["detect_direction"] = "true"
            # ocr_options["probability"] = "true"
            # ocr_options["language_type"] = "ENG"
            # ocr_json = client.basicAccurate(img_src)
            # print(ocr_json)
            # if ocr_json.get('words_result_num', None) == 1:
            # ocr_result = ocr_json.get('words_result')[0].get('+words')
            print('机器人检测OCR结果为', ocr_result)
            captcha_row_url = "https://www.amazon.com/errors/validateCaptcha?"
            captcha_url = captcha_row_url + "&amzn=" + amzn_code + "&amzn-r=" + amzn_r_code + "&field-keywords=" + \
                          ocr_result
            self.s.get(captcha_url)

        print(self.s.headers.get('User-Agent', '未知请求头'))
        if str(res.status_code) != '200':
            print('访问页面{}时出错'.format(url))
            print("页面错误，状态码为：", res.status_code)
            try:
                print(etree.HTML(res.text).xpath('//title/text()')[0])
            except Exception as e:
                print(e)
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
            if self.begin >= 5:
                print('该链接:' + url + '访问出错次数超过5次,可能该链接下没有同类商品内容')
                self.undo_list.append(url)
                return
            self.get_detail(url)

        # print(self.begin)
        self.begin = 0
        # 类别
        kinds = res_html.xpath("//div[@class='twisterTextDiv text']/span[@class='a-size-base' and 1]/text()")[:]

        # sort_list = []
        if not kinds:
            kinds = res_html.xpath('//div[@class="a-section a-spacing-none twisterShelf_displaySection"]/span/text()')[
                    :]

        # 不同类别、颜色、款式的编号
        # sorts_codes = res_html.xpath('//*[starts-with(@id, "size_name")]/@data-defaultasin')[:]
        # color_sorts = res_html.xpath('//*[starts-with(@id, "color_name")]/@data-defaultasin')[:]
        # style_sorts = res_html.xpath('//*[starts-with(@id, "style_name")]/@data-defaultasin')[:]
        # sort_list = sorts_codes + color_sorts + style_sorts

        try:
            # 这种方式不能获取所有的子ASIN 只能获取某个颜色、尺寸、款式下的默认ASIN
            # 要获取所有的ASIN 请调用Keepa
            sorts_codes = res_html.xpath('//*[starts-with(@id, "size_name")]/@data-defaultasin')[:]
            color_sorts = res_html.xpath('//*[starts-with(@id, "color_name")]/@data-defaultasin')[:]
            style_sorts = res_html.xpath('//*[starts-with(@id, "style_name")]/@data-defaultasin')[:]
            sort_list_raw = sorts_codes + color_sorts + style_sorts
            sort_list = list(set(sort_list_raw))

            # asin_patt = re.compile("dp/(.*)/")
            #
            # sort_list = [re.search(asin_patt, each).groups()[0] for each in sort_list_raw if each]
            # sort_list = list(set(sort_list))
        except:
            sort_list = []

        try:
            choosen_kinds = res_html.xpath('//div[starts-with(@id, "variation")]/div/span/text()')
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
                key = each.xpath("string(.//th)")
                # print(key, "---")
                value = each.xpath("string(.//td)")
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
                key = each.xpath("string(./th)")
                # print(key, "---")
                value = each.xpath("string(./td)")
                # print(key, value)
                if key and value:
                    key = key.replace("\n", '').replace("\t", '').strip()
                    value = value.replace("\n", '').replace("\t", '').strip()
                    if key != "Customer Reviews":
                        item[key] = value

        if res_html.xpath("//table[@id='productDetails_techSpec_section_1']"):
            print("model-4")
            for each in res_html.xpath("//table[@id='productDetails_techSpec_section_1']//tr"):
                key = each.xpath("string(.//th)")
                # print(key, "---")
                value = each.xpath("string(.//td)")
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
                key = each.xpath("string(.//td[@class='label'])")
                # print(key, "---")
                value = each.xpath("string(.//td[@class='value'])")
                # print(key, "---", value)
                if key and value:
                    key = key.replace("\n", '').replace("\t", '').strip()
                    value = value.replace("\n", '').replace("\t", '').strip()
                    if key != "Customer Reviews":
                        item[key] = value
                        print(key, "---", value)

        # 图片路径
        try:
            goods_pic_url = res_html.xpath('//img[@id="landingImage"]/@src')[0]
        except:
            goods_pic_url = None

        ASIN = item.get('ASIN', None)

        try:
            multi_asin = set(sort_list.append(ASIN))
        except:
            multi_asin = set(sort_list)
        print("-----------")
        print(multi_asin)
        print("-----------")
        product_dimensions = item.get('Product Dimensions', None)
        package_dimensions = item.get('Package Dimensions', None)
        product_weight = item.get('Item Weight', None)
        date_on_shelf = item.get('Date first listed on Amazon', None)

        if product_weight:
            product_weight = weight_handle(product_weight)
        ship_weight = item.get('Shipping Weight', None)
        if ship_weight:
            ship_weight = weight_handle(ship_weight)

        feature_list = res_html.xpath("//div[@id='feature-bullets']/ul/li/span/text()")
        features = []
        for feature in feature_list:
            feature = feature.strip()
            features.append(feature)

        rank_in_HK = None
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
                    goods_rank_num = int(goods_rank_num.replace(',', '').strip())
                except:
                    pass
                goods_rank_sort = re.sub(weight_str, '', goods_rank_sort)
                goods_each_ranks[goods_rank_sort.strip()] = goods_rank_num
                if re.search('Home & Kitchen', goods_rank_sort):
                    try:
                        rank_in_HK = int(goods_rank_num)
                    except:
                        rank_in_HK = None

            self.rank_list.append(goods_each_ranks)
            print(self.rank_list[-1])

            try:
                category_main = list(self.rank_list[-1].keys())[0]
                rank_main = int(list(self.rank_list[-1].values())[0])
            except:
                category_main, rank_main = None, None
            print(category_main, rank_main)
        # 评价数量
        try:
            goods_review_count = \
            res_html.xpath('//div[@id="averageCustomerReviews"]//span[@id="acrCustomerReviewText"]/text()')[0]
            goods_review_count = int(goods_review_count.split(" ")[0].replace(",", ""))
        except:
            goods_review_count = 0

        # 评价星级
        try:

            goods_review_star = res_html.xpath('//div[@id="averageCustomerReviews"]//span[@class="a-icon-alt"]/text()')[
                0]
            goods_review_star = float(goods_review_star.split(" ")[0])
        except:
            goods_review_star = None

        # 高频评价
        fre_words = res_html.xpath('//*[@id="cr-lighthut-1-"]/div/span/a/span/text()')[:]
        high_fre_words = [each.strip() for each in fre_words if each]

        try:
            goods_price = res_html.xpath("//span[starts-with(@id,'priceblock')]/text()")[0]
        except:
            goods_price = None

        import json
        try:
            brand = res_html.xpath('//a[@id="bylineInfo"]/text()')[0]
        except:
            brand = None
        try:
            buy_box_info = res_html.xpath('//*[@id="turboState"]/script/text()')[0]
            buy_box_json = json.loads(buy_box_info)
            stockOnHand = buy_box_json['eligibility']['stockOnHand']
        except:
            stockOnHand = None

        # 卖方
        try:
            seller = res_html.xpath('string(//div[@id="merchant-info"])')
            if not seller:
                try:
                    seller = res_html.xpath('string(//span[@id="merchant-info"])')
                except:
                    seller = None
            if re.search('Reviews', seller):
                seller = seller.replace("\n", "").split("Reviews")[0].strip()
            if re.search(r"P.when", seller):
                seller = seller.replace("\n", "").split("P.when")[0].strip()
            seller = seller.replace("\n", "").strip()
        except:
            seller = None

        try:
            seller_cls = seller_handle(seller)
        except:
            seller_cls = None

        sales_est = None

        # 销量修正，实际反馈发现，销量预测头部偏高，中部偏低，做出微调
        if category_main and rank_main:
            try:
                sales_est = int(get_sales(cate=category_main, rank=rank_main))
                # if sales_est >= 2000:
                #     sales_est = int(sales_est * 1)
                # elif sales_est >= 1000:
                #     sales_est = int(sales_est * 1.15)
                # elif sales_est >= 500:
                #     sales_est = int(sales_est * 1)
                # else:
                #     sales_est = int(sales_est * 0.75)
                # time.sleep(random.random())
                # print("sales:", sales_est)
            except:
                pass

        each_detail_list = (
            goods_pic_url, goods_title, ASIN, brand, ad_plus, goods_price, choose_kind, seller, seller_cls, sales_est,
            rank_in_HK, date_on_shelf, stockOnHand, goods_review_count, product_dimensions, package_dimensions,
            product_weight, ship_weight, goods_review_star, category_main, rank_main, high_fre_words, multi_asin,
            goods_each_ranks)

        if goods_title:
            self.detail_list.append(each_detail_list)

    def run(self, data_path):
        if data_path.endswith('xlsx'):
            data = pd.read_excel(data_path, encoding='utf-8')
            for asin in data['asin']:
                if asin:
                    url = "https://www.amazon.com/dp/" + str(asin)
                    self.url_queue.put(url)
                    print(self.url_queue.qsize())
        if data_path.endswith('csv'):
            data = pd.read_csv(data_path, encoding='utf-8')
            for url in data['goods_url_full']:
                if url:
                    self.url_queue.put(url)
                    print(self.url_queue.qsize())

        while True:
            try:
                thread_list = [threading.Thread(target=goods_detail.get_detail, args=(self.url_queue.get(),)) for i in range(20)
                               if not self.url_queue.empty()]
                time.sleep(random.uniform(2, 4))

                for each in thread_list:
                    self.s.headers.update({'User-Agent': random.choice(self.head_user_agent)})
                    try:
                        time.sleep(random.random())
                        each.start()
                        print(each.name)
                    except Exception as e:
                        print(e)

                for each in thread_list:
                    each.join()

            except Exception as e:
                print(e)
            if self.url_queue.empty():
                break
        details_pd = pd.DataFrame(goods_detail.detail_list,
                                  columns=['goods_pic_url', 'goods_title', 'ASIN', 'brand', 'ad_plus', 'goods_price',
                                             'choose_kind', 'seller', 'seller_cls','sales_est','rank_in_HK', 'date_on_shelf',
                                           'stockOnHand', 'goods_review_count', 'product_dimensions', 'package_dimensions',
                                           'product_weight', 'ship_weight', 'goods_review_star', 'category_main', 'rank_main'
                                           , 'high_fre_words','multi_asin','goods_each_ranks'])

        aft = datetime.datetime.now().strftime('%m%d%H%M')

        for base_code_full, ASIN in zip(details_pd['goods_pic_url'], details_pd['ASIN']):
            if base_code_full and ASIN:
                try:
                    base_code = base_code_full.split(',')[1]
                    pic_save(base_code, ASIN)
                except Exception as e:
                    print("图片存储错误：", base_code_full, e)

        time.sleep(3)
        domain_path = os.path.abspath('../')
        details_pd['pic_url'] = domain_path + r"\data\pic\\" + details_pd['ASIN'] + ".jpg"
        details_pd['pic_table_url'] = '<table> <img src=' + '\"' + details_pd['pic_url'] + '\"' + 'height="140" >'
        details_pd.sort_values(by=['sales_est'], inplace=True, ascending=False)
        file_name_new = "../data/goods_detail/" + aft + "_with_ad.xlsx"
        details_pd.drop_duplicates(subset=['category_main', 'rank_main'], inplace=True)
        details_pd.to_excel(file_name_new, encoding='utf-8')
        # print("以下链接未能正确解析，请手动查证")
        for each in self.undo_list:
            print(each)


def weight_handle(weight):
    # 把kg ounce pound 都转化为数字存储
    weight = weight.lower().replace(',', '')
    if re.search("kg", weight):
        weight_int = float(weight.split(' ')[0]) * 1000

    elif re.search("ounce", weight):
        weight_int = float(weight.split(' ')[0]) * 28.35

    elif re.search("pound", weight):
        weight_int = float(weight.split(' ')[0]) * 453.60

    else:
        try:
            weight_int = float(weight.split(' ')[0])
        except:
            weight_int = weight
    return weight_int


def feature_handle(feature):
    import re
    patt = re.compile('(\d+)[^\d+]*[by\*x]\s*(\d+)')
    res = re.search(patt, feature.lower()).groups()
    return res


def seller_handle(seller):
    # 卖家类型识别
    if not seller:
        return None
    else:
        if re.search('sold by Amazon.com', seller, re.I):
            return 'AMZ'
        elif re.search('Fulfilled by Amazon', seller, re.I):
            return 'FBA'
        else:
            return 'FBM'


def get_sales(rank, cate="Home & Kitchen"):
    import requests
    import urllib
    s = requests.Session()
    row_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }
    sales_url = "https://amzscout.net/extensions/scoutlite/v1/sales?"
    full_url = sales_url + "domain=COM&category=" + urllib.parse.quote(cate)+ "&rank=" + str(rank)
    print(full_url)
    s.headers.update(row_headers)
    res = s.get(full_url, timeout=10)
    try:
        return res.json().get('sales')
    except:
        return None


def pic_save(base_code, ASIN):

    import base64
    img_data = base64.b64decode(base_code)
    file = open(r"..\data\pic\\" + str(ASIN) + '.jpg', 'wb')
    file.write(img_data)
    file.close()


if __name__ == '__main__':

    goods_detail = GoodDetail()
    data_path = r"../data/goods_rank_list/wind chimes_11261110_with_ad.csv"
    goods_detail.run(data_path)
