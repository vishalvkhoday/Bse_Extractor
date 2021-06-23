'''
Created on Nov 25, 2020

@author: DELL
'''

from scrapy.selector import Selector
from scrapy.http import HtmlResponse
from scrapy.http import response
from scrapy.http

Selector(text = body).xpath('//*[@id="liveindexTable"]/tbody').extract()
response = HtmlResponse(url="https://www.nseindia.com/market-data/live-market-indices",body=body)
# Selector(response=response).xpath('//*[@id="liveindexTable"]/tbody').extract()

response.selector.xpath('//*[@id="liveindexTable"]/tbody').extract()

Request.
# import scrapy
# from scrapy.spiders import CrawlSpider,Rule
# from scrapy.linkextractors import LinkExtractor
#  
#  
# class NseTicker(CrawlSpider):
#     name="Quotes"
#     allowed_domain = ["www.nseindia.com/market-data/live-market-indices"]
#     start_url = ["https://www.nseindia.com/market-data/live-market-indices"]
#     rules=(
#         Rule(LinkExtractor(allow=(),restrict_xpath=('//*[@id="liveindexTable"]/tbody'),)),callback="parse_item",follow=True),)
#     