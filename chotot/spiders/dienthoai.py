# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from datetime import datetime
from chotot.items import Dienthoai
import leveldb

db = leveldb.LevelDB("dienthoai")

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

class DienthoaiSpider(scrapy.Spider):
    name = 'dienthoai'
    start_urls = ['http://www.chotot.com/toan-quoc/mua-ban-dien-thoai/']
    custom_settings = {'FEED_URI': "chotot_dienthoai_%(time)s.csv",
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
        while (next_page_number < 3):
            absolute_next_page_url = 'https://www.chotot.com/toan-quoc/mua-ban-dien-thoai?page=' + str(
                next_page_number)
            next_page_number = next_page_number + 1
            yield Request(absolute_next_page_url, callback=self.parse)

    def parse_item(self, response):
        item = Dienthoai()
        id = response.request.url.split('/')[-1].split('.')[0]
        title = response.xpath('//*[@id="__next"]/div/div[1]/div/div[3]/div[2]/div[1]/h1/text()').extract()[1]
        # title = response.xpath('//*[@class="adTilte___3UqYW]/text()').extract_first()
        url = response.request.url
        price = response.xpath('//*[@itemprop="price"]/text()').extract_first()
        tel = response.xpath('//*[@id="call_phone_btn"]/@href').extract_first().replace('tel:', '')
        district = response.xpath('//*[@class="fz13"]/text()').extract_first()
        seller = response.xpath(
            '//*[@id="__next"]/div/div[1]/div/div[4]/div/div[2]/div[1]/div/a/div[2]/div[1]/div/b/text()').extract_first()
        seller_type = response.xpath('//*[@class="inforText___1ELFe"]/p/text()').extract_first()
        posted_time = response.meta.get('time')

        # datetime object containing current date and time
        now = datetime.now()

        crawled_time = now.strftime("%d/%m/%Y %H:%M:%S")

        mobile_attributes = response.xpath('//*[@class="media-body media-middle"]/span/span/text()').extract()

        brand = ""
        status = ""
        storage = ""
        series = ""
        color = ""
        ship = ""
        guarantee = ""

        for attr in mobile_attributes:
            index = mobile_attributes.index(attr)
            if (attr == "Hãng: "):
                brand = mobile_attributes[index+1]

            elif (attr == "Tình trạng: "):
                status = mobile_attributes[index+1]

            elif (attr == "Dung lượng: "):
                storage = mobile_attributes[index+1]

            elif (attr == "Dòng máy: "):
                series = mobile_attributes[index+1]

            elif (attr == "Màu sắc: "):
                color = mobile_attributes[index+1]

            elif (attr == "Giao hàng tận nơi: "):
                ship = mobile_attributes[index+1]

            elif (attr == "Tình trạng bảo hành: "):
                guarantee = mobile_attributes[index+1]

        item['id'] = id
        item['url'] = url
        item['title'] = title
        item['price'] = price
        item['tel'] = tel
        item['district'] = district
        item['seller'] = seller
        item['seller_type'] = seller_type
        item['crawled_time'] = crawled_time
        item['posted_time'] = posted_time

        item['brand'] = brand
        item['status'] = status
        item['storage'] = storage
        item['series'] = series
        item['color'] = color
        item['ship'] = ship
        item['guarantee'] = guarantee

        try:
            exist = search(item)
        except:
            insert(item)
            yield item
