# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LaMaisonItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ProductItem(scrapy.Item):
    Nom = scrapy.Field()
    Marque = scrapy.Field()
    Prix = scrapy.Field()
    url = scrapy.Field()
