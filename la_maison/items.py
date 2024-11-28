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
    id_produit =scrapy.Field()
    nom_produit =scrapy.Field()
    marque_produit =scrapy.Field()
    prix_produit =scrapy.Field()
    categorie =scrapy.Field()
    sous_categorie =scrapy.Field()
    sous_sous_categorie =scrapy.Field()
    description = scrapy.Field()
    reference =scrapy.Field()
    code_article =scrapy.Field()
    gencod =scrapy.Field()
    url_produit =scrapy.Field()

class categorieItem(scrapy.Item):
    nom_sous_sous_categorie = scrapy.Field()
    url = scrapy.Field()
    sous_categorie = scrapy.Field()
    categorie = scrapy.Field()
