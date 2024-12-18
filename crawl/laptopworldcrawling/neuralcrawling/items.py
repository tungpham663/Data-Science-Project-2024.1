# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NeuralcrawlingItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    manufacturer = scrapy.Field()
    cpu_manufacturer = scrapy.Field()   
    cpu_brand_modifier = scrapy.Field()
    cpu_generation = scrapy.Field()
    cpu_speed = scrapy.Field()
    ram = scrapy.Field()
    ram_type = scrapy.Field()
    bus = scrapy.Field()
    storage = scrapy.Field()
    screen_size = scrapy.Field()
    screen_resolution = scrapy.Field()
    #refresh_rate = scrapy.Field()
    gpu_manufacturer = scrapy.Field()
    weight = scrapy.Field()
    battery = scrapy.Field()
    price = scrapy.Field()
