# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from datetime import datetime
from chotot.items import Oto
import leveldb

db = leveldb.LevelDB("db/oto")

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


class OtoSpider(scrapy.Spider):
    name = 'oto'
    start_urls = ['http://xe.chotot.com/mua-ban-oto/']
    custom_settings = {'FEED_URI': "output/chotot_oto_%(time)s.csv",
                       'FEED_FORMAT': 'csv'}


    def parse(self, response):
        item_urls = response.xpath('//*[@class="styles__AdItemLayout-sc-1s892rt-0 gMQvHZ"]/li/a/@href').extract()
        item_urls = item_urls[5:]
        item_infos = response.xpath('//*[@class="styles__AdDescriptionBox-sc-11gq2ty-6 deXxdP"]/span/text()').extract()

        posted_time = []

        # for item_info in item_infos:
        #     out = {'info': item_info}
        #     yield out

        # for item_url in item_urls:
        #     out = {'info': item_url}
        #     yield out

        for item_info in item_infos:
            if validate_time(item_info):
                posted_time.append(item_info)

        for item_url in item_urls:
            index = item_urls.index(item_url)
            item_url = 'https://xe.chotot.com' + item_url

            yield Request(item_url, callback=self.parse_item, meta={'time': posted_time[index]})

        next_page_number = 2
        while (next_page_number < 3):
            absolute_next_page_url = 'https://xe.chotot.com/mua-ban-oto?page=' + str(
                next_page_number)
            next_page_number = next_page_number + 1
            yield Request(absolute_next_page_url, callback=self.parse)

    def parse_item(self, response):
        item = Oto()
        id = response.request.url.split('/')[-1].split('.')[0]
        title = response.xpath('//h1[@class="styles__Title-sc-14jh840-1 lgidFF"]/text()').extract_first()
        url = response.request.url
        price = response.xpath('//*[@itemprop="price"]/text()').extract_first()
        tel = response.xpath('//*[@id="call_phone_btn"]/@href').extract_first().replace('tel:', '')
        district = response.xpath('//*[@class="fz13"]/text()').extract_first()
        seller = response.xpath(
            '//*[@class="styles__NameDiv-jjbnsh-3 bWjZeW"]/b/text()').extract_first()
        seller_type = response.xpath('//*[@class="styles__InfoItem-jjbnsh-10 rkcJk"]/p/text()').extract_first()
        posted_time = response.meta.get('time')

        # datetime object containing current date and time
        now = datetime.now()

        crawled_time = now.strftime("%d/%m/%Y %H:%M:%S")

        attributes = response.xpath('//*[@class="media-body media-middle"]/span/text()').extract()

        brand = ""
        produced_year = "Field()"
        status = ""
        fuel = ""
        seed_count = ""
        series = ""
        km_count = ""
        transmission = ""
        design = ""
        video = ""
        made_in = ""

        for attr in attributes:
            index = attributes.index(attr)
            if (attr == "Hãng: "):
                brand = attributes[index+1]

            elif (attr == "Năm sản xuất: "):
                produced_year = attributes[index+1]

            elif (attr == "Tình trạng: "):
                status = attributes[index+1]

            elif (attr == "Nhiên liệu: "):
                fuel = attributes[index+1]

            elif (attr == "Số chỗ: "):
                seed_count = attributes[index+1]

            elif (attr == "Dòng xe: "):
                series = attributes[index+1]

            elif (attr == "Số Km đã đi: "):
                km_count = attributes[index+1]

            elif (attr == "Hộp số: "):
                transmission = attributes[index+1]

            elif (attr == "Kiểu dáng: "):
                design = attributes[index + 1]

            elif (attr == "Người bán gửi Video: "):
                video = attributes[index + 1]

            elif (attr == "Xuất xứ: "):
                made_in = attributes[index + 1]

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
        item['produced_year'] = produced_year
        item['status'] = status
        item['fuel'] = fuel
        item['seed_count'] = seed_count
        item['series'] = series
        item['km_count'] = km_count
        item['transmission'] = transmission
        item['design'] = design
        item['video'] = video
        item['made_in'] = made_in

        try:
            exist = search(item)
        except:
            insert(item)
            yield item
