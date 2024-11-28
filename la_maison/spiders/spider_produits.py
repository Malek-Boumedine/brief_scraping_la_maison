import scrapy
from la_maison.items import ProductItem
import json
import re

class ProduitsSpider(scrapy.Spider):
    name = "spider_produits"
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            'id_produit',
            'nom_produit',
            'marque_produit',
            'prix_produit',
            "en_promotion",
            'date_fin_promo',
            'categorie',
            'sous_categorie',
            'sous_sous_categorie',
            'description',
            'reference',
            'code_article',
            'gencod',
            'url_produit'
        ]
    }
    
    def start_requests(self):
        with open("categories.json", "r") as fichier : 
            self.donnees = json.load(fichier)
            
        for objet in self.donnees:
            yield scrapy.Request(
                url=objet["url"],
                callback=self.parse_product,
                meta={
                    "categorie" : objet["categorie"],
                    "sous_categorie" : objet["sous_categorie"],
                    "sous_sous_categorie" : objet["nom_sous_sous_categorie"]
                }
            )

    def parse_product(self, response):
        liste_produits = response.css('ol.products.list')
        produits = liste_produits.css('li.item.product')
        
        for p in produits : 
            if p.css('div div strong a::text').get():
                url_produit = p.css('div a::attr(href)').get()

                yield response.follow(url_produit, callback=self.parse_page_produit, meta={
                    "url_produit" : url_produit,
                    "categorie" : response.meta["categorie"],
                    "sous_categorie" : response.meta["sous_categorie"],
                    "sous_sous_categorie" : response.meta["sous_sous_categorie"],
                })
                
        bouton_suivant = response.css('a.action.next::attr(href)').get()
        if bouton_suivant :
            url_suivante = response.urljoin(bouton_suivant)
            yield scrapy.Request(
                url = url_suivante, 
                callback = self.parse_product,
                meta = response.meta)
        
    def parse_page_produit(self, response):
        nom_produit = response.css('h1.page-title span::text').get()
        prix_produit = response.css('div.product-info-price div span span::attr(data-price-amount)').get()
        id_produit = response.css('div.product-info-price div::attr(data-product-id)').get()
        description = response.css('div.product-info-short-description::text').get()
        
        attributs_produit = response.css('div.product.attribute div::text').get()
        if attributs_produit : 
            regex_reference = r"Référence\s*:\s*(\S+)"
            match_reference = re.search(regex_reference, attributs_produit)
            reference = match_reference.group(1) if match_reference else None
            
            regex_code_article = r"Code article\s*:\s*(\S+)"
            match_code_article = re.search(regex_code_article, attributs_produit)
            code_article = match_code_article.group(1) if match_code_article else None
        else : 
            reference = "null"
            code_article = "null"
        code_gen = response.xpath('.//dd[@data-th="Gencod"]/text()').get()
        gencod = code_gen.split("|")[0] if code_gen else "Null"
        marque = response.css('div.manufacturer a::attr(title)').get()
        marque_produit = marque if marque else "Null"
        
        categorie_meta = response.meta["categorie"]
        sous_categorie_meta = response.meta["sous_categorie"]
        sous_sous_categorie_meta = response.meta["sous_sous_categorie"]
        liste_cats = response.css('ul.items li')
        product_promo = response.css('div.product-info-price div.price-box.price-final_price div span.offer-validity::text').get()
        regex = r"\d{2}/\d{2}/\d{4}"
        date_fin_promo = re.search(regex, product_promo).group() if product_promo else None
        
        if categorie_meta : 
            categorie = categorie_meta
        else :
            categorie = liste_cats[1].css('a::attr(title)').get()
            
        if sous_categorie_meta : 
           sous_categorie = sous_categorie_meta
        else : 
            sous_categorie = liste_cats[2].css('a::attr(title)').get()
           
        if sous_sous_categorie_meta : 
            sous_sous_categorie = sous_sous_categorie_meta
        else : 
            sous_sous_categorie = liste_cats[3].css('a::attr(title)').get()
            
        yield ProductItem(
            id_produit = id_produit,
            nom_produit = nom_produit,
            marque_produit = marque_produit,
            prix_produit = prix_produit,
            en_promotion = "Oui"if product_promo else "Non",
            date_fin_promo = date_fin_promo,
            categorie = categorie,
            sous_categorie = sous_categorie,
            sous_sous_categorie = sous_sous_categorie,
            
            description = description,
            reference = reference,
            code_article = code_article,
            gencod = gencod,
            url_produit = response.meta["url_produit"])
