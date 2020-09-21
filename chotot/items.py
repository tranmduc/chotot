# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.loader import ItemLoader
from scrapy.loader.processors import Compose, TakeFirst

to = Compose(TakeFirst())

class Xemay(Item):
    id = Field()
    url = Field()
    title = Field()
    price = Field()
    tel = Field()
    district = Field()
    seller = Field()
    seller_type = Field()
    crawled_time = Field()
    posted_time = Field()
    brand = Field()
    registered_year = Field()
    status = Field()
    volume = Field()
    series = Field()
    km_count = Field()
    type = Field()
    video = Field()

class Vieclam(Item):
    id = Field()
    url = Field()
    title = Field()
    salary = Field()
    tel = Field()
    district = Field()
    seller = Field()
    seller_type = Field()
    crawled_time = Field()
    posted_time = Field()
    salary_type = Field()
    job_field = Field()
    gender = Field()
    quantity = Field()
    certi_skill = Field()
    max_age = Field()
    job_type = Field()
    experience = Field()
    company = Field()
    education = Field()
    min_age = Field()
    bonus = Field()

class Mevabe(Item):
    id = Field()
    url = Field()
    title = Field()
    price = Field()
    tel = Field()
    district = Field()
    seller = Field()
    seller_type = Field()
    crawled_time = Field()
    posted_time = Field()

class MyItemLoader(ItemLoader):
    default_item_class = Mevabe
    id_out = to
    url_out = to
    title_out = to
    price_out = to
    tel_out = to
    district_out = to
    seller_out = to
    seller_type_out = to
    crawled_time_out = to
    posted_time_out = to

class Pet(Item):
    id = Field()
    url = Field()
    title = Field()
    price = Field()
    tel = Field()
    district = Field()
    seller = Field()
    seller_type = Field()
    crawled_time = Field()
    posted_time = Field()

class MyItemLoaderPet(ItemLoader):
    default_item_class = Pet
    id_out = to
    url_out = to
    title_out = to
    price_out = to
    tel_out = to
    district_out = to
    seller_out = to
    seller_type_out = to
    crawled_time_out = to
    posted_time_out = to

class Dienthoai(Item):
    id = Field()
    url = Field()
    title = Field()
    price = Field()
    tel = Field()
    district = Field()
    seller = Field()
    seller_type = Field()
    crawled_time = Field()
    posted_time = Field()

    brand = Field()
    status = Field()
    storage = Field()
    series = Field()
    color = Field()
    ship = Field()
    guarantee = Field()

class Xe(Item):
    id = Field()
    url = Field()
    title = Field()
    price = Field()
    tel = Field()
    district = Field()
    seller = Field()
    seller_type = Field()
    crawled_time = Field()
    posted_time = Field()
    type = Field()

class generalItem(Item):
    id = Field()
    url = Field()
    title = Field()
    price = Field()
    tel = Field()
    district = Field()
    seller = Field()
    seller_type = Field()
    crawled_time = Field()
    posted_time = Field()