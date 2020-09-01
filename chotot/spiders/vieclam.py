# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from datetime import datetime
from chotot.items import Vieclam
import leveldb

db = leveldb.LevelDB("vieclam")

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

class VieclamSpider(scrapy.Spider):
    name = 'vieclam'
    start_urls = ['http://www.chotot.com/toan-quoc/danh-sach-viec-lam/']
    custom_settings = {'FEED_URI': "chotot_vieclam_%(time)s.csv",
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
            absolute_next_page_url = 'https://www.chotot.com/toan-quoc/danh-sach-viec-lam?page=' + str(
                next_page_number)
            next_page_number = next_page_number + 1
            yield Request(absolute_next_page_url, callback=self.parse)

    def parse_item(self, response):
        item = Vieclam()
        id = response.request.url.split('/')[-1].split('.')[0]
        title = response.xpath('//*[@id="__next"]/div/div[1]/div/div[3]/div[2]/div[1]/h1/text()').extract()[1]
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

        job_attributes = response.xpath('//*[@class="media-body media-middle"]/span/span/text()').extract()

        salary_type = ""
        job_field = ""
        gender = ""
        quantity = ""
        certi_skill = ""
        max_age = ""
        job_type = ""
        experience = ""
        company = ""
        education = ""
        min_age = ""
        bonus = ""

        for attr in job_attributes:
            index = job_attributes.index(attr)
            if (attr == "Hình thức trả lương: "):
                salary_type = job_attributes[index+1]

            elif (attr == "Ngành nghề: "):
                job_field = job_attributes[index+1]

            elif (attr == "Giới tính: "):
                gender = job_attributes[index+1]

            elif (attr == "Số lượng tuyển dụng: "):
                quantity = job_attributes[index+1]

            elif (attr == "Chứng chỉ / kỹ năng: "):
                certi_skill = job_attributes[index+1]

            elif (attr == "Tuổi tối đa: "):
                max_age = job_attributes[index+1]

            elif (attr == "Loại công việc: "):
                job_type = job_attributes[index+1]

            elif (attr == "Kinh nghiệm: "):
                experience = job_attributes[index+1]

            elif (attr == "Tên công ty: "):
                company = job_attributes[index+1]

            elif (attr == "Học vấn tối thiểu: "):
                education = job_attributes[index+1]

            elif (attr == "Các quyền lợi khác: "):
                bonus = job_attributes[index+1]

            elif (attr == "Tuổi tối thiểu: "):
                min_age = job_attributes[index+1]

        item['id'] = id
        item['url'] = url
        item['title'] = title
        item['salary'] = price
        item['tel'] = tel
        item['district'] = district
        item['seller'] = seller
        item['seller_type'] = seller_type
        item['crawled_time'] = crawled_time
        item['posted_time'] = posted_time

        item['salary_type'] = salary_type
        item['job_field'] = job_field
        item['gender'] = gender
        item['quantity'] = quantity
        item['certi_skill'] = certi_skill
        item['max_age'] = max_age
        item['job_type'] = job_type
        item['experience'] = experience
        item['company'] = company
        item['education'] = education
        item['min_age'] = min_age
        item['bonus'] = bonus

        try:
            exist = search(item)
        except:
            insert(item)
            yield item
