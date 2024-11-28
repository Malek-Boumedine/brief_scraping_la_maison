import scrapy
from la_maison.items import categorieItem



class CategoriesSpider(scrapy.Spider):
    name = "spider_categories"
    custom_settings = {
        'FEED_EXPORT_FIELDS': [
            "nom_categorie",
            "url",
            "page_list"
        ]
    }

    start_urls = ["https://www.lamaison.fr/"]

    def parse(self, response):
        categories = response.css('li.level1')

        bonnes_affaires = response.css('li.level0.nav-5.last')
        url_bonnes_affaires = bonnes_affaires.css('a::attr(href)').get()
        nom_bonnes_affaires = bonnes_affaires.css('a span::text').get()

        for cat in categories :

            dict_cat = {
                "nom_cat" : cat.css('a span::text').get(),
                "url_cat" : cat.css('a::attr(href)').get(),
                "page_list" : False,
                "sous_categories" : []
            }
            
            yield categorieItem(
                nom_categorie = cat.css('a span::text').get(),
                url = cat.css('a::attr(href)').get(),
                page_list = False,
            )

            sous_categories = cat.css('li.level2')
            for s_cat in sous_categories :
                dict_ss_cat = {
                    "nom_ss_cat" : s_cat.css('a span::text').get(),
                    "url_ss_cat" : s_cat.css('a::attr(href)').get(),
                    "page_list" : False,
                    "sous_sous_categories" : []
                }
                dict_cat["sous_categories"].append(dict_ss_cat)
                
                yield categorieItem(
                    nom_categorie = s_cat.css('a span::text').get(),
                    url = s_cat.css('a::attr(href)').get(),
                    page_list = False,
                )

                sous_sous_categories = s_cat.css('li.level3')
                for s_menu in sous_sous_categories :
                    dict_sous_sous_categorie = {
                        "nom_categorie" : s_menu.css('a span::text').get(),
                        "url" : s_menu.css('a::attr(href)').get(),
                        "page_list" : True,
                        "sous_categorie" : s_cat.css('a span::text').get(),
                        "categorie" : cat.css('a span::text').get(),
                    }
                    dict_ss_cat["sous_sous_categories"].append(dict_sous_sous_categorie)
                    
                    yield categorieItem(
                        nom_categorie = s_menu.css('a span::text').get(),
                        url = s_menu.css('a::attr(href)').get(),
                        page_list = True,
                    )

                    
                    # yield categorieItem(
                    #     nom_categorie = dict_sous_sous_categorie["nom_categorie"],
                    #     url = dict_sous_sous_categorie["url"],
                    #     sous_categorie = dict_sous_sous_categorie["sous_categorie"],
                    #     categorie = dict_sous_sous_categorie["categorie"]
                    # )


        yield categorieItem(
            nom_categorie = nom_bonnes_affaires,
            url = url_bonnes_affaires,
            page_list = True
        )



