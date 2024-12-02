# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    id_produit = scrapy.Field()
    nom_produit = scrapy.Field()
    marque_produit = scrapy.Field()
    prix_produit = scrapy.Field()
    en_promotion = scrapy.Field()
    date_fin_promo = scrapy.Field()
    categorie = scrapy.Field()
    sous_categorie = scrapy.Field()
    sous_sous_categorie = scrapy.Field()
    id_sous_sous_categorie = scrapy.Field()
    reference = scrapy.Field()
    code_article = scrapy.Field()
    gencod = scrapy.Field()
    url_produit = scrapy.Field()


class categorieItem(scrapy.Item):
    identifiant = scrapy.Field()
    nom_categorie = scrapy.Field()
    type_cat = scrapy.Field()
    url = scrapy.Field()
    id_parent = scrapy.Field()


