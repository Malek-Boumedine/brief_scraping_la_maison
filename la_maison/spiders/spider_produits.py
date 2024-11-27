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
            if p.css('div div strong a::text').get() :  
                nom_produit = p.css('div div strong a::text').get()
                marque_produit = p.css('div div div.brand a::text').get()
                prix_produit = p.css('div div div.product-item-details-wrapper div span span span::text').get()
                url_produit = p.css('div a::attr(href)').get()
                folow_produit = response.follow(url_produit, callback=self.parse_page_product)
                yield ProductItem(Nom=nom_produit, Marque=marque_produit, Prix=prix_produit, url=url_produit)
        
        bouton_suivant = response.css('a.action.next::attr(href)').get()
        if bouton_suivant : 
            page_suivante = response.urljoin(bouton_suivant)
            yield scrapy.Request(url = page_suivante, callback=self.parse_product)
            
        
    def parse_page_product(self, response):
        page_produit = response.css('.columns .column.main')
        reference_produit = page_produit.css('div.product-view-top')
        pass
            