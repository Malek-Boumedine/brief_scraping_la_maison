# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class LaMaisonPipeline:
    def __init__(self):
        self.connexion = sqlite3.connect("laMaison.db")
        self.curseur = self.connexion.cursor()
        self.ids_seen = set() 
        
    def creer_tables_categories(self) : 
        self.curseur.execute("""CREATE TABLE IF NOT EXISTS categories(
            "id" INT PRIMARY KEY,
            "nom" VARCHAR(200) NOT NULL,
            "url" TEXT NOT NULL
            )""")

    def creer_table_sous_categories(self):
        self.curseur.execute("""CREATE TABLE IF NOT EXISTS sous_categories(
            "id" INT PRIMARY KEY,
            "nom" VARCHAR(200) NOT NULL,
            "url" TEXT NOT NULL,
            "id_parent" INT NOT NULL,
            FOREIGN KEY (id_parent) REFERENCES categorie(id)
            )""")

    def creer_table_page_list(self):
        self.curseur.execute("""CREATE TABLE IF NOT EXISTS page_list(
            "id" INT PRIMARY KEY,
            "nom" VARCHAR(200) NOT NULL,
            "url" TEXT NOT NULL,
            "id_parent" INT NOT NULL,
            FOREIGN KEY (id_parent) REFERENCES sous_categories(id)
            )""")

    def creer_table_marque(self):
        self.curseur.execute("""CREATE TABLE IF NOT EXISTS marque(
            "id" INT PRIMARY KEY,
            "nom" VARCHAR(250) NOT NULL,
            )""")

    # def creer_table_produits(self):
    #     self.curseur.execute("""CREATE TABLE IF NOT EXISTS produits(
    #         "id_produit" INT PRIMARY KEY,
    #         "nom_produit" VARCHAR(250) NOT NULL,
    #         "id_marque" INT,
    #         "prix_produit" DOUBLE NOT NULL,
    #         "en_promotion" BOOL NOT NULL,
    #         "date_fin_promo" DATE,
    #         "id_sous_sous_categorie" INT NOT NULL,
    #         "reference" VARCHAR(100),
    #         "code_article" VARCHAR(100),
    #         "gencod" INT,
    #         "url_produit" TEXT NOT NULL,
    #         FOREIGN KEY (id_marque) REFERENCES marque(id)
    #         FOREIGN KEY (id_categorie) REFERENCES page_list(id)
    #         )""")

    def creer_table_produits(self):
        self.curseur.execute("""CREATE TABLE IF NOT EXISTS produits(
            "id_produit" INT PRIMARY KEY,
            "nom_produit" VARCHAR(250) NOT NULL,
            "marque_produit" INT,
            "prix_produit" DOUBLE NOT NULL,
            "en_promotion" BOOL NOT NULL,
            "date_fin_promo" DATE,
            "id_page_list" INT NOT NULL,
            "reference" VARCHAR(100),
            "code_article" VARCHAR(100),
            "gencod" INT,
            "url_produit" TEXT NOT NULL,
            FOREIGN KEY (id_page_list) REFERENCES page_list(id)
            )""")

    def is_produit_doublon(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["id_produit"] in self.ids_seen:
            print("ma logique si doublon")
        else:
            self.ids_seen.add(adapter["id_produit"])
            return item

    def process_item(self, item, spider):
        self.creer_tables_categories()
        self.creer_table_sous_categories()
        self.creer_table_page_list()
        self.creer_table_produits()
        
        if "id_produit" in item : 
            if item["id_produit"] not in self.ids_seen:
                self.curseur.execute("""INSERT OR IGNORE INTO produits VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                (item["id_produit"], item["nom_produit"], item["marque_produit"], item["prix_produit"],
                                item["en_promotion"], item["date_fin_promo"], item["id_sous_sous_categorie"], item["reference"], item["code_article"], item["gencod"],
                                item["url_produit"]))
                self.connexion.commit()
        
        elif item["type_cat"] == "CAT" : 
            self.curseur.execute("""INSERT OR IGNORE INTO categories VALUES(?, ?, ?)""",
                            (item["identifiant"], item["nom_categorie"], item["url"]))
            self.connexion.commit()

        elif item["type_cat"] == "CAT":
            self.curseur.execute("""
                                 INSERT OR IGNORE INTO categories VALUES(?, ?,
                                                                         ?)""",
                                 (item["identifiant"],
                                  item["nom_categorie"],
                                  item["url"]))
            self.connexion.commit()

        elif item["type_cat"] == "S_CAT":
            self.curseur.execute("""
                                 INSERT OR IGNORE INTO sous_categories
                                 VALUES(?, ?, ?, ?)""",
                                 (item["identifiant"],
                                  item["nom_categorie"],
                                  item["url"],
                                  item["id_parent"]))
            self.connexion.commit()

        elif item["type_cat"] == "PAGE_LIST":
            self.curseur.execute("""
                                 INSERT OR IGNORE INTO page_list
                                 VALUES(?, ?,?, ?)""",
                                 (item["identifiant"],
                                  item["nom_categorie"],
                                  item["url"],
                                  item["id_parent"]))
            self.connexion.commit()

        return item
