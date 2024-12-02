import scrapy
from la_maison.items import categorieItem



class CategoriesSpider(scrapy.Spider):
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

    def parse(self, response):
        categories = response.css('li.level1')

        bonnes_affaires = response.css('li.level0.nav-5.last')
        url_bonnes_affaires = bonnes_affaires.css('a::attr(href)').get()
        nom_bonnes_affaires = bonnes_affaires.css('a span::text').get()
        
        id_categorie = 1
        id_sous_categorie = 1
        id_page_list = 1

        for cat in categories:

            dict_cat = {
                "nom_cat" : cat.css('a span::text').get(),
                "url_cat" : cat.css('a::attr(href)').get(),
                "sous_categories" : []
            }
            
            yield categorieItem(                # enregistrer les infos des catégories
                identifiant = id_categorie,
                nom_categorie = cat.css('a span::text').get(),
                type_cat = "CAT",
                url = cat.css('a::attr(href)').get(),
                id_parent = None
            )

            sous_categories = cat.css('li.level2')
            for s_cat in sous_categories :
                dict_ss_cat = {
                    "nom_ss_cat" : s_cat.css('a span::text').get(),
                    "url_ss_cat" : s_cat.css('a::attr(href)').get(),
                    "sous_sous_categories" : []
                }
                dict_cat["sous_categories"].append(dict_ss_cat)
                
                yield categorieItem(            # enregistrer les infos des sous_catégories
                    identifiant = id_sous_categorie,
                    nom_categorie = s_cat.css('a span::text').get(),
                    type_cat = "S_CAT",
                    url = s_cat.css('a::attr(href)').get(),
                    id_parent = id_categorie
                )

                sous_sous_categories = s_cat.css('li.level3')
                for s_menu in sous_sous_categories :
                    dict_sous_sous_categorie = {
                        "nom_categorie" : s_menu.css('a span::text').get(),
                        "url" : s_menu.css('a::attr(href)').get(),
                        "sous_categorie" : s_cat.css('a span::text').get(),
                        "categorie" : cat.css('a span::text').get(),
                    }
                    dict_ss_cat["sous_sous_categories"].append(dict_sous_sous_categorie)
                    
                    yield categorieItem(        # # enregistrer les infos des sous_sous_catégories
                        identifiant = id_page_list,
                        nom_categorie = s_menu.css('a span::text').get(),
                        type_cat = "PAGE_LIST",
                        url = s_menu.css('a::attr(href)').get(),
                        id_parent = id_sous_categorie
                    )
                    id_page_list += 1
                id_sous_categorie += 1
            id_categorie += 1
        
        yield categorieItem(                    # enregistrer les infos des bonnes affaires
            identifiant = id_page_list,
            nom_categorie = nom_bonnes_affaires,
            type_cat = None,
            url = url_bonnes_affaires,
            id_parent = None
        )




