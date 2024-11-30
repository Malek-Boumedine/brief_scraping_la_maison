import scrapy
from items import ProductItem
import json


with open('categories.json', 'r') as f:
    JSON_CATEGORIES = json.load(f)

liste_urls = []
for objet in JSON_CATEGORIES:
    liste_urls.append(objet["url"])


class ProduitsSpider(scrapy.Spider):
    name = "spider_produits"
    start_urls = liste_urls  # URL initiale

    def parse(self, response):
        for url in self.start_urls:
            if url:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_product
                )
            else:
                continue

    def parse_product(self, response):
        liste_produits = response.css('ol.products.list')
        produits = liste_produits.css('li.item.product')
        if liste_produits not in [None, ""] and produits not in [None, ""]:
            for p in produits:
                if p.css('div div strong a::text').get():
                    nom_produit = p.css('div div strong a::text').get()
                    if p.css('div div div.brand a::text').get():
                        marque_produit = p.css(
                            'div div div.brand a::text').get()
                    else:
                        marque_produit = nom_produit.split()[-1]
                    prix_produit = p.css('div div div.product-item-details-wrapper div span span span::text').get()
                    url_produit = p.css('div a::attr(href)').get()
                    yield response.follow(url_produit,
                                          callback=self.parse_page_produit,
                                          meta={
                                                "nom_produit": nom_produit,
                                                "marque_produit": marque_produit,
                                                "prix_produit": prix_produit,
                                                "url_produit": url_produit
                                            })

        bouton_suivant = response.css('a.action.next::attr(href)').get()
        if bouton_suivant:
            url_suivante = response.urljoin(bouton_suivant)
            yield scrapy.Request(url=url_suivante, callback=self.parse_product)

    def parse_page_produit(self, response):
        attributs_produit = response.css(
            'div.product.attribute div::text').get()
        if attributs_produit != "":
            if attributs_produit in [" "]:
                liste_attributs = attributs_produit.split()
                reference = liste_attributs[2]
                code_article = liste_attributs[-1]
            else:
                reference = f"undefined string : {attributs_produit}"
                code_article = f"undefined string : {attributs_produit}"
        else:
            reference = None
            code_article = None

        if response.xpath('.//dd[@data-th="Gencod"]/text()').get():
            gencod = response.xpath('.//dd[@data-th="Gencod"]/text()').get()
        else:
            gencod = "null"

        yield ProductItem(
            nom_produit=response.meta["nom_produit"],
            marque_produit=response.meta["marque_produit"],
            prix_produit=response.meta["prix_produit"],
            reference=reference,
            code_article=code_article,
            gencod=gencod,
            url_produit=response.meta["url_produit"])
