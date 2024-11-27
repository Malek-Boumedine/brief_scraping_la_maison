import scrapy


class CategoriesSpider(scrapy.Spider):
    name = "spider_categories"
    # allowed_domains = ["www.lamaison.fr"]
    start_urls = ["https://www.lamaison.fr/"]

    def parse(self, response):
        titre = response.xpath("//title/text()").get()
        categories = response.css('li.level1')

        resultat = {"titre" : titre, "categories" : []}
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
                    "sous_menus" : []
                }
                dict_cat["sous_categories"].append(dict_ss_cat)

                sous_menus = s_cat.css('li.level3')
                for s_menu in sous_menus :
                    dict_sous_menu = {
                        "nom_ss_menu" : s_menu.css('a span::text').get(),
                        "url_ss_menu" : s_menu.css('a::attr(href)').get(),
                        "id_ss_menu" : s_menu.css('::attr(id)').get(),
                    }
                    dict_ss_cat["sous_menus"].append(dict_sous_menu)
            resultat["categories"].append(dict_cat)
        yield resultat


