# -*- coding: utf-8 -*-
import scrapy
import re

class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/110287/']

    def parse(self, response):

        title = response.xpath('//*[@id="post-110287"]/div[1]/h1/text()').extract()[0]
        create_date = response.xpath('//*[@id="post-110287"]/div[2]/p/text()').extract()[0].strip().replace('·','').strip()
        praise_num = response.xpath("//span[contains(@class,'vote-post-up')]/h10/text()").extract()[0]
        fav_num = response.xpath("//span[contains(@class,'bookmark-btn')]/text()").extract()[0].strip()
        match_re = re.match(".*?(\d+).*",fav_num)
        if match_re:
            fav_num = match_re.group(1)

        comment_num = response.xpath("//a[@href='#article-comment']/span/text()").extract()[0].strip()
        match_re = re.match(".*?(\d+).*",comment_num)
        if match_re:
            comment_num = match_re.group(1)

        content = response.xpath("//div[@class='entry']").extract()[0]
        tag_list = response.xpath("//p[@class='entry-meta-hide-on-mobile']/a/text()").extract()
        tag_list = [element for element in tag_list if not element.strip().endwith("评论")]
        tags = ",".join(tag_list)
        pass
