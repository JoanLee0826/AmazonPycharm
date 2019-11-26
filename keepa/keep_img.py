import pandas as pd
import requests
import random

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
            ]


def pic_save(img_url, ASIN):
    s = requests.Session()
    s.headers.update({'User-Agent': random.choice(head_user_agent)})
    res = s.get(img_url)
    if str(res.status_code) == '200':
        img_data = res.content
        with open(r"..\data\pic\\" + str(ASIN) + '.jpg', 'wb') as f:
            f.write(img_data)
            f.close()

def get_pic(file_path):
    data = pd.DataFrame(pd.read_excel(file_path))
    data['pic'] = data['Image'].apply(lambda x: x.split(';')[0])

    data['table_pic'] = '<table> <img src=' + data['pic'] + ' height="140" >'
    data.to_excel(file_path.replace('.xlsx', '_with_pic.xlsx'), encoding='utf-8', engine='xlsxwriter')


if __name__ == '__main__':
    file_path = r'E:\爬虫pycharm\data\category\Keepa_ASIN_Export.2019_10_29.1366_products.xlsx'
    get_pic(file_path)