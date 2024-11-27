import scrapy
from items import ProductItem

class ProduitsSpider(scrapy.Spider):
    name = "spider_produits"
    start_urls = ["https://www.lamaison.fr/bricolage/outillage/outil-electroportatif.html"]  # URL initiale

    def parse(self, response):
        
        yield scrapy.Request(
            url=self.start_urls[0],
            callback=self.parse_product
        )
        
    
    def parse_product(self, response):
        liste_produits = response.css('ol.products.list')
        produits = liste_produits.css('li.item.product')
        
        for p in produits : 
            if p.css('div div strong a::text').get():
                nom_produit = p.css('div div strong a::text').get()
                if p.css('div div div.brand a::text').get() :
                    marque_produit = p.css('div div div.brand a::text').get()
                else :
                    marque_produit = nom_produit.split()[-1]
                prix_produit = p.css('div div div.product-item-details-wrapper div span span span::text').get()
                url_produit = p.css('div a::attr(href)').get()
                yield response.follow(url_produit, callback=self.parse_page_produit, meta={
                    "nom_produit" : nom_produit,
                    "marque_produit" : marque_produit,
                    "prix_produit" : prix_produit,
                    "url_produit" : url_produit
                })
                
        bouton_suivant = response.css('a.action.next::attr(href)').get()
        if bouton_suivant :
            url_suivante = response.urljoin(bouton_suivant)
            yield scrapy.Request(url=url_suivante, callback=self.parse_product)
        
        
    def parse_page_produit(self, response):
        attributs_produit = response.css('div.product.attribute div::text').get()
        liste_attributs = attributs_produit.split()
        reference = liste_attributs[2]
        code_article = liste_attributs[-1]
        if response.xpath('.//dd[@data-th="Gencod"]/text()').get() : 
            gencod = response.xpath('.//dd[@data-th="Gencod"]/text()').get()
        else : 
            gencod = "null"

        
        yield ProductItem(
            nom_produit = response.meta["nom_produit"],
            marque_produit = response.meta["marque_produit"],
            prix_produit = response.meta["prix_produit"],
            reference = reference,
            code_article = code_article,
            gencod = gencod,
            url_produit = response.meta["url_produit"])
