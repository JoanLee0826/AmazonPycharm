import requests
from lxml import etree
from aip import AipOcr


APP_ID = '11240997'
API_KEY = '6ZU9O51SKfbaZyg0vzAUWXqN'
SECRET_KEY = 'xtCepeZVrdZ6LSHBDf0xNhYq7PEdY8No '
client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
url = 'https://www.amazon.com'


def robot_check(res_html):
    s = requests.Session()
    s.headers.update({})
    res = s.get(url)
    res_row_html = etree.HTML(res.text)
    title = res_row_html.xpath("//title/text()")[0]
    if title == 'Robot Check':
        img_src = res_row_html.xpath("//div[@class='a-row a-text-center']/img/@src")[0]
        print("验证码图片链接：", img_src)
        amzn_code = res_row_html.xpath("//input[@name='amzn']")[0].get('value')
        amzn_r_code = res_row_html.xpath("//input[@name='amzn-r']")[0].get('value')
        ocr_options = {}
        ocr_options["detect_direction"] = "true"
        ocr_options["probability"] = "true"
        ocr_options["language_type"] = "ENG"
        ocr_json = client.basicAccurate(img_src)
        print(ocr_json)
        if ocr_json.get('words_result_num', None) == 1:
            ocr_result = ocr_json.get('words_result')[0].get('+words')
            print('机器人检测OCR结果为', ocr_result)
            captcha_row_url = "https://www.amazon.com/errors/validateCaptcha?"
            captcha_url = captcha_row_url + "&amzn=" + amzn_code + "&amzn-r=" + amzn_r_code + "&field-keywords=" + \
                          ocr_result
            s.get(captcha_url)