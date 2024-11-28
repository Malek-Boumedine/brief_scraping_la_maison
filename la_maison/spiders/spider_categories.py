import scrapy
from la_maison.items import categorieItem



class CategoriesSpider(scrapy.Spider):
    name = "spider_categories"
    # allowed_domains = ["www.lamaison.fr"]
    start_urls = ["https://www.lamaison.fr/"]

    def parse(self, response):
        categories = response.css('li.level1')

        for cat in categories :
            dict_cat = {
                "nom_cat" : cat.css('a span::text').get(),
                "url_cat" : cat.css('a::attr(href)').get(),
                "id_cat" : cat.css('::attr(id)').get(),
                "sous_categories" : []
            }

            sous_categories = cat.css('li.level2')
            for s_cat in sous_categories :
                dict_ss_cat = {
                    "nom_ss_cat" : s_cat.css('a span::text').get(),
                    "url_ss_cat" : s_cat.css('a::attr(href)').get(),
                    "id_ss_cat" : s_cat.css('::attr(id)').get(),
                    "sous_sous_categories" : []
                }
                dict_cat["sous_categories"].append(dict_ss_cat)

                sous_sous_categories = s_cat.css('li.level3')
                for s_menu in sous_sous_categories :
                    dict_sous_sous_categorie = {
                        "nom_sous_sous_categorie" : s_menu.css('a span::text').get(),
                        "url" : s_menu.css('a::attr(href)').get(),
                        "sous_categorie" : s_cat.css('a span::text').get(),
                        "categorie" : cat.css('a span::text').get(),
                    }
                    dict_ss_cat["sous_sous_categories"].append(dict_sous_sous_categorie)
                    yield dict_sous_sous_categorie
                    


