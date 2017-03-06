# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy import Request, FormRequest
from scrapy.utils.request import request_fingerprint
from ResearchGateSpider.items import ResearchGateItem
from ResearchGateSpider.datafilter import DataFilter
from ResearchGateSpider.func import parse_text_by_multi_content
from scrapy.exceptions import CloseSpider
#from scrapy_splash import SplashRequest
#from scrapy_splash import SplashMiddleware
import hashlib
import time


class RGSpider1(CrawlSpider):
    name = 'RGSpider1'
    #name = "ResearchGateSpider"
    domain = 'https://www.researchgate.net'
    start_urls = ["https://www.researchgate.net/login"]
    # pub_item = []
    # finger_print = ''
    # start_urls = ['https://www.researchgate.net/profile/Anahid_A_Birjandi/contributions']

    def start_requests(self):
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
        }
        alphabet_list = ["A", "B", "C", "D",
                         "E", "F", "G", "H",
                         "I", "J", "K", "L", 
                         "M", "N", "O", "P",
                         "Q", "R", "S", "T",
                         "U", "V", "W", "X",
                         "Y", "Z", "Other"]
        for alphabet in alphabet_list:
            url = "https://www.researchgate.net/directory/profiles/"+alphabet
            yield Request(url, headers=headers, callback=self.parse_profile_directory, dont_filter=True)
            #break

        # url = "https://www.researchgate.net/directory/profiles/" + alphabet_list[0]
        # print url
        # yield Request(url, callback=self.parse_profile_directory, dont_filter=True)

    def parse_profile_directory(self, response):
        if response.status == 429:
            lostitem_str = 'first level directory: ' + 'response.url\n'
            self.lostitem_file.write(lostitem_str)
            self.lostitem_file.close()
            raise CloseSpider(reason=u'被封了，准备切换ip')
        headers = response.request.headers
        headers["referer"] = response.url
        for url in response.xpath(
                '//ul[contains(@class, "list-directory")]/descendant::a/@href'). \
                extract():
            url = self.domain + "/" + url
            yield Request(url, headers=headers, callback=self.parse_profile_directory2, dont_filter=True)
            #break

        # urls = response.xpath('//ul[contains(@class, "list-directory")]/descendant::a/@href').extract()
        # url0 = self.domain + "/" + urls[0]
        # print url0
        # yield Request(url0, callback=self.parse_profile_directory2, dont_filter=True)

    def parse_profile_directory2(self, response):
        if response.status == 429:
            lostitem_str = 'second level directory: ' + 'response.url\n'
            self.lostitem_file.write(lostitem_str)
            self.lostitem_file.close()
            raise CloseSpider(reason='被封了，准备切换ip')
        headers = response.request.headers
        headers["referer"] = response.url
        for url in response.xpath(
                '//ul[contains(@class, "list-directory")]/descendant::a/@href'). \
                extract():
            url = self.domain + "/" + url
            yield Request(url, headers=headers, callback=self.parse_profile_directory3, dont_filter=True)
            #break
        # urls = response.xpath('//ul[contains(@class, "list-directory")]/descendant::a/@href').extract()
        # url0 = self.domain + "/" + urls[0]
        # print url0
        # yield Request(url0, callback=self.parse_profile_directory3, dont_filter=True)

    def parse_profile_directory3(self, response):
        if response.status == 429:
            lostitem_str = 'third level directory: ' + 'response.url\n'
            self.lostitem_file.write(lostitem_str)
            self.lostitem_file.close()
            raise CloseSpider(reason='被封了，准备切换ip')
        headers = response.request.headers
        headers["referer"] = response.url
        person_selectors = response.xpath('//ul[contains(@class, "list-directory")]/li')
        for person in person_selectors:
            item = ResearchGateItem()
            item['fullname'] = DataFilter.simple_format(person.xpath('.').extract())
            person_url = self.domain + '/' + DataFilter.simple_format(person.xpath('./a/@href').extract())
            item['link'] = person_url
            item['person_key'] = hashlib.sha256(person_url).hexdigest()
            yield item
        # for url in response.xpath(
        #         '//ul[contains(@class, "list-directory")]/li'). \
        #         extract():
        #     url = self.domain + "/" + url
        #     yield Request(url, headers=headers, callback=self.parse_candidate_overview, dont_filter=True)
             #break
        #urls = response.xpath('//ul[contains(@class, "list-directory")]/descendant::a/@href').extract()
        #url0 = self.domain + "/" + urls[1]
        #print url0
        #yield Request(url0, headers=headers, callback=self.parse_candidate_overview, dont_filter=True)

    def __init__(self, **kwargs):
        super(RGSpider1, self).__init__(**kwargs)
        self.lostitem_file = open('1.out', 'a+')
        pass

    def close(self, reason):
        self.lostitem_file.close()
        super(RGSpider1, self).close(self, reason)
