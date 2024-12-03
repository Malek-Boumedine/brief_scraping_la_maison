import scrapy
from selenium import webdriver
from la_maison.items import categorieItem
from typing import Generator



class CategoriesSpider(scrapy.Spider) :
    """
    CategoriesSpider est un spider Scrapy qui extrait des informations sur les catégories du site La Maison. 
    Il navigue sur le site et génère des données structurées pour les catégories, sous-catégories et offres spéciales.

    Ce spider commence à l'URL principale et utilise Selenium pour rendre le contenu de la page. 
    Il analyse ensuite le HTML pour extraire les détails des catégories, y compris les identifiants, les noms, les URL et les relations parent-enfant entre les catégories.

    Attributs :
        name (str) : Le nom du spider, utilisé par Scrapy pour l'identifier.
        custom_settings (dict) : Paramètres personnalisés pour l'exportation des données du spider, y compris les champs à exporter.
        start_urls (list) : Les URL initiales à partir desquelles commencer le scraping, dans ce cas, le site principal de La Maison.

    Méthodes :
        start_requests() : Génère les requêtes initiales à envoyer aux URL de départ.
        parse(response) : Analyse la réponse du site web et génère des éléments de catégorie.

    Args :
        response (scrapy.http.Response) : L'objet de réponse contenant le contenu HTML de la page.

    Yields :
        categorieItem : Un élément structuré contenant des informations sur la catégorie, y compris :
            - identifiant (str) : L'identifiant unique de la catégorie.
            - nom_categorie (str) : Le nom de la catégorie.
            - type_cat (str) : Le type de catégorie (par exemple, "CAT", "S_CAT", "PAGE_LIST").
            - url (str) : L'URL de la catégorie.
            - id_parent (str ou None) : L'identifiant de la catégorie parente, le cas échéant.
    """
        
    name = "spider_categories"
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            "identifiant",
            "nom_categorie",
            "type_cat",
            "url",
            "id_parent"
        ]
    }
    
    start_urls = ["https://www.lamaison.fr/"]
    

    def parse(self, response) -> Generator[categorieItem, None, None]:
        """
        Analyse la réponse du site La Maison pour extraire les informations sur les catégories et sous-catégories. 
        Cette fonction utilise Selenium pour rendre la page et Scrapy pour sélectionner et produire des données de catégorie structurées.

        La méthode `parse` récupère les catégories principales, les sous-catégories et les bonnes affaires du site web. 
        Elle produit des éléments contenant des identifiants, des noms, des URL et des relations parent-enfant pour chaque niveau de catégorie.

        Args:
            response (scrapy.http.Response): L'objet de réponse contenant le contenu HTML de la page.

        Yields:
            categorieItem: Un élément structuré contenant des informations sur la catégorie, y compris :
                - identifiant (str): L'identifiant unique de la catégorie.
                - nom_categorie (str): Le nom de la catégorie.
                - type_cat (str): Le type de la catégorie (par exemple, "CAT", "S_CAT", "PAGE_LIST").
                - url (str): L'URL de la catégorie.
                - id_parent (str ou None): L'identifiant de la catégorie parente, le cas échéant.

        Notes:
            - Cette méthode utilise Selenium pour charger dynamiquement le contenu de la page, ce qui peut entraîner des temps de chargement plus longs.
            - Assurez-vous que le driver Chrome est correctement configuré et que le chemin d'accès est défini dans votre environnement.
            - En cas d'absence de certaines informations (par exemple, si un élément n'est pas trouvé), les valeurs retournées peuvent être `None`.
        """
        
        driver = webdriver.Chrome()
        driver.get("https://www.lamaison.fr/")
        driver.implicitly_wait(10)
        sel = scrapy.Selector(text=driver.page_source)      # Créer un nouveau sélecteur avec le contenu de Selenium

        categories = sel.css('li.level1')
        bonnes_affaires = sel.css('li.level0.nav-5.last')
        id_bonnes_affaires = bonnes_affaires.css('a::attr(id)').get()
        url_bonnes_affaires = bonnes_affaires.css('a::attr(href)').get()
        nom_bonnes_affaires = bonnes_affaires.css('a span::text').get()
        
        
        for cat in categories : 

            id_categorie = cat.css('::attr(id)').get()
            nom_categorie = cat.css('a span::text').get()
            url_categorie = cat.css('a::attr(href)').get()
            
            yield categorieItem(                # enregistrer les infos des catégories
                identifiant = id_categorie,
                nom_categorie = nom_categorie,
                type_cat = "CAT",
                url = url_categorie,
                id_parent = None
            )

            sous_categories = cat.css('li.level2')
            
            for s_cat in sous_categories :
                
                id_sous_categorie = s_cat.css('::attr(id)').get()
                nom_ss_catcategorie = s_cat.css('a span::text').get()
                url_ss_catcategorie = s_cat.css('a::attr(href)').get()
 
                yield categorieItem(            # enregistrer les infos des sous_catégories
                    identifiant = id_sous_categorie,
                    nom_categorie = nom_ss_catcategorie,
                    type_cat = "S_CAT",
                    url = url_ss_catcategorie,
                    id_parent = id_categorie
                )

                sous_sous_categories = s_cat.css('li.level3')
                
                for s_menu in sous_sous_categories :
                    
                    id_page_list = s_menu.css('::attr(id)').get()
                    nom_page_list = s_menu.css('a span::text').get()
                    url_page_list = s_menu.css('a::attr(href)').get()
                    
                    yield categorieItem(        # # enregistrer les infos des sous_sous_catégories
                        identifiant = id_page_list,
                        nom_categorie = nom_page_list,
                        type_cat = "PAGE_LIST",
                        url = url_page_list,
                        id_parent = id_sous_categorie
                    )
        
        yield categorieItem(                    # enregistrer les infos des bonnes affaires
            identifiant = id_bonnes_affaires,
            nom_categorie = nom_bonnes_affaires,
            type_cat = "PAGE_LIST",
            url = url_bonnes_affaires,
            id_parent = None
        )
