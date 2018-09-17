# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NhadatSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url=scrapy.Field()
    house_link=scrapy.Field()
    house_location=scrapy.Field()
    house_name=scrapy.Field()
    house_area=scrapy.Field()
    num_bedroom=scrapy.Field()
    date_posted=scrapy.Field()
    house_price=scrapy.Field()
    house_price_area=scrapy.Field()
    pass

class NhadatPropertyItem(scrapy.Item):
    url=scrapy.Field()
    house_name=scrapy.Field()
    house_usable_area=scrapy.Field()
    house_price=scrapy.Field()
    house_price_per_area=scrapy.Field()
    house_code=scrapy.Field()
    house_location=scrapy.Field()
    num_floors=scrapy.Field()
    num_bedrooms=scrapy.Field()
    num_toilets=scrapy.Field()
    year_of_construction=scrapy.Field()
    deposit=scrapy.Field()
    direction=scrapy.Field()
    road_info=scrapy.Field()
    juridical=scrapy.Field()
    project=scrapy.Field()
    utilities=scrapy.Field()
    num_utilities=scrapy.Field()
    description=scrapy.Field()
    pass