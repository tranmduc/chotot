# -*- coding: utf-8 -*-
import scrapy

import scrapy
from scrapy.http import Request
from datetime import datetime
from chotot.items import Pet, MyItemLoaderPet
import leveldb

db = leveldb.LevelDB("db/pet")

def insert(item):
     db.Put(item['id'].encode('UTF-8'), item['tel'].encode('UTF-8'))


def search(item):
    query = db.Get(item['id'].encode('UTF-8'))
    return query.decode()

def validate_time(string):
    if string == "Tin ưu tiên" or string.find("trước") > -1:
        return True
    else:
        return False

class PetSpider(scrapy.Spider):
    name = 'pet'
    start_urls = ['http://www.chotot.com/toan-quoc/mua-ban-thu-cung/']
    custom_settings = {'FEED_URI': "output/chotot_pet_%(time)s.csv",
                       'FEED_FORMAT': 'csv'}

    def parse(self, response):
        item_urls = response.xpath('//a[@class="adItem___2GCVQ"]/@href').extract()
        item_infos = response.xpath('//span[@class="item___eld8Q"]/text()').extract()

        posted_time = []

        for item_info in item_infos:
            if validate_time(item_info):
                posted_time.append(item_info)

        for item_url in item_urls:
            index = item_urls.index(item_url)
            item_url = 'https://www.chotot.com' + item_url

            yield Request(item_url, callback=self.parse_item, meta={'time': posted_time[index]})

        next_page_number = 2
        while (next_page_number < 1979):
            absolute_next_page_url = 'https://www.chotot.com/toan-quoc/mua-ban-thu-cung?page=' + str(
                next_page_number)
            next_page_number = next_page_number + 1
            yield Request(absolute_next_page_url, callback=self.parse)

    def parse_item(self, response):
        loader = MyItemLoaderPet(selector=response)
        id = response.request.url.split('/')[-1].split('.')[0]
        title = response.xpath('//*[@id="__next"]/div/div[1]/div/div[3]/div[2]/div[1]/h1/text()').extract()[1]
        url = response.request.url
        price = response.xpath('//*[@itemprop="price"]/text()').extract_first()
        tel = response.xpath('//*[@id="call_phone_btn"]/@href').extract_first().replace('tel:', '')
        district = response.xpath('//*[@class="fz13"]/text()').extract_first()
        seller = response.xpath(
            '//*[@class="nameDiv___2aJ46"]/b/text()').extract_first()
        seller_type = response.xpath('//*[@class="inforText___1ELFe"]/p/text()').extract_first()
        posted_time = response.meta.get('time')

        # datetime object containing current date and time
        now = datetime.now()

        crawled_time = now.strftime("%d/%m/%Y %H:%M:%S")

        loader.add_value('id', id)
        loader.add_value('tel', tel)
        loader.add_value('title', title)
        loader.add_value('url', url)
        loader.add_value('price', price)
        loader.add_value('district', district)
        loader.add_value('seller', seller)
        loader.add_value('seller_type', seller_type)
        loader.add_value('posted_time', posted_time)
        loader.add_value('crawled_time', crawled_time)

        try:
            exist = search(loader.load_item())
        except:
            insert(loader.load_item())
            yield loader.load_item()
