import scrapy
from la_maison.items import ProductItem
import csv
import re
from typing import Generator



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
            'reference',
            'code_article',
            'gencod',
            'url_produit'
        ]
    }
    
    
    def start_requests(self) -> Generator[scrapy.Request, None, None] :
        """
        Génère des requêtes de démarrage pour récupérer des pages de produits à partir d'un fichier CSV.

        Cette méthode lit un fichier CSV contenant des catégories et envoie des requêtes HTTP pour les lignes où le type de catégorie est 'PAGE_LIST'. Chaque requête est associée à un identifiant pour un traitement ultérieur.

        Args:
            self: L'instance de la classe.

        Returns:
            Un générateur de requêtes Scrapy pour les pages de produits.
        """
        
        with open("categories.csv", newline="") as fichier:
            donnees_categories = csv.DictReader(fichier, delimiter=",")
            for ligne in donnees_categories :
                if ligne["type_cat"] == "PAGE_LIST" :
                    yield scrapy.Request(url=ligne["url"],callback=self.parse_product, meta={"identifiant": ligne["identifiant"]})


    def parse_product(self, response) -> Generator[scrapy.Request, None, None] :
        """
        Analyse la réponse d'une page de produits et extrait les informations des produits.

        Cette méthode récupère une liste de produits à partir de la réponse d'une page, en suivant les liens vers les pages de détails des produits. Elle gère également la pagination en suivant le lien vers la page suivante si disponible.

        Args:
            self: L'instance de la classe.
            response: La réponse de la requête contenant les informations sur les produits.

        Returns:
            Un générateur de requêtes Scrapy pour les pages de détails des produits et pour la pagination.
        """

        liste_produits = response.css('ol.products.list')
        produits = liste_produits.css('li.item.product')
        
        for p in produits:
            if p.css('div div strong a::text').get():
                url_produit = p.css('div a::attr(href)').get()
                yield response.follow(url_produit, callback=self.parse_page_produit,meta={"url_produit" : url_produit, "identifiant": response.meta["identifiant"]})
                
        bouton_suivant = response.css('a.action.next::attr(href)').get()
        if bouton_suivant :
            url_suivante = response.urljoin(bouton_suivant)
            yield scrapy.Request(url = url_suivante, callback = self.parse_product, meta = response.meta)

        
    def parse_page_produit(self, response) -> Generator[ProductItem, None, None] :
        """
        Analyse la page d'un produit et extrait ses informations détaillées.

        Cette méthode récupère divers attributs d'un produit à partir de la réponse d'une page, y compris le nom, le prix, l'identifiant, les références, et les catégories associées. Elle crée ensuite un objet `ProductItem` contenant toutes ces informations pour un traitement ultérieur.

        Args:
            self: L'instance de la classe.
            response: La réponse de la requête contenant les détails du produit.

        Returns:
            Un générateur d'objets `ProductItem` avec les informations extraites du produit.
        """

        nom_produit = response.css('h1.page-title span::text').get()
        prix_produit = response.css('div.product-info-price div span span::attr(data-price-amount)').get()
        id_produit = response.css('div.product-info-price div::attr(data-product-id)').get()
        
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
        
        liste_cats = response.css('ul.items li')
        product_promo = response.css('div.product-info-price div.price-box.price-final_price div span.offer-validity::text').get()
        regex = r"\d{2}/\d{2}/\d{4}"
        date_fin_promo = re.search(regex, product_promo).group() if product_promo else None
        
        categorie = liste_cats[1].css('a::attr(title)').get()
        sous_categorie = liste_cats[2].css('a::attr(title)').get()
        sous_sous_categorie = liste_cats[3].css('a::attr(title)').get()
            
        yield ProductItem(
            id_produit = id_produit,
            nom_produit = nom_produit,
            marque_produit = marque_produit,
            prix_produit = prix_produit,
            en_promotion = True if product_promo else False,
            date_fin_promo = date_fin_promo,
            categorie = categorie,
            sous_categorie = sous_categorie,
            sous_sous_categorie = sous_sous_categorie,
            id_sous_sous_categorie = response.meta["identifiant"],
            reference = reference,
            code_article = code_article,
            gencod = gencod,
            url_produit = response.meta["url_produit"])
