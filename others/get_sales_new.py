
def get_sales(rank, cate="Home & Kitchen"):
    import requests
    import urllib
    s = requests.Session()
    row_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
    }
    sales_url = "https://amzscout.net/extensions/scoutlite/v1/sales?"
    full_url = sales_url + "domain=COM&category="+ urllib.parse.quote(cate)+ "&rank=" + str(rank)
    print(full_url)
    s.headers.update(row_headers)
    res = s.get(full_url)
    return (res.json().get('sales'))

if __name__ == '__main__':
    get_sales(rank='2689')