# -*- coding: utf-8 -*-
import scrapy
import re

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['http://www.zhihu.com/']
    agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    headers = {
        "Accept":"*/*",
        "Accept-Encoding":"gzip, deflate, br",
        "Accept-Language":"zh-CN,zh;q=0.8",
        "X-Requested-With":"XMLHttpRequest",
        "HOST": "www.zhihu.com",
        "Origin": "https: // www.zhihu.com",
        "Referer": "https://www.zhihu.com/",
        "User-Agent": agent
    }

    def parse(self, response):
        pass

    def start_requests(self):
        return [scrapy.Request('https://www.zhihu.com/#signin',headers=self.headers,callback=self.login)]


    def login(self,response):
        response_text = response.text
        match_obj = re.search('.*name="_xsrf" value="(.*?)"', response_text,re.DOTALL)
        xsrf = ''
        if match_obj:
            xsrf = match_obj.group(1)
        if xsrf:
            post_url = "https://www.zhihu.com/login/phone_num"
            post_data = {
                "_xsrf": xsrf,
                "password": '07943688365',
                "captcha_type": 'cn',
                "photo_num": '13537751102'
            }
        return [scrapy.FormRequest(
            url=post_url,
            formdata=post_data,
            headers=self.headers,
            callback=self.check_login
        )]


    def check_login(self,response):
        # 验证服务器返回的数据是否成功
        login_code = eval(response.text)
        print(login_code['msg'])
        pass
