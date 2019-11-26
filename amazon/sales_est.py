import numpy as np
import pandas as pd


def get_sales(rank, cate="Home & Kitchen"):
    import requests
    import urllib

    s = requests.Session()
    # proxies = {
    #     "http": "http://180.118.247.88:9000"
    # }
    row_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }
    raw_url = "https://amzscout.net/"
    s.get(raw_url, headers=row_headers)

    test_header ={
        "Host": "amzscout.net",
        "Connection": "keep-alive",
        "Content-Length": "49",
        "Origin": "https://amzscout.net",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "*/*",
        "Referer": "https://amzscout.net/sales-estimator/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    test_url = "https://amzscout.net/analytics/v1/events"
    data = 'category=Estimator&action=search&software=LANDING'
    s.post(url=test_url, headers=test_header, data=data)

    url = "amzscout.net/extensions/scoutlite/v1/sales?domain=COM&category=" + urllib.parse.quote(cate)+ "&rank=" + str(rank)
    ams_headers = {
        "Host": "amzscout.net",
        "Connection":"keep-alive",
        "Cache-Control":"max-age=0",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.9",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin"
    }
    try:
        s.headers.update(ams_headers)
        res = s.get(url, headers=ams_headers)
        return res.json().get('sales')
    except:
        return None

if __name__ == '__main__':

    print(get_sales(cate="Baby",rank=2658))


