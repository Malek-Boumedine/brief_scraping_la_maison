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
            id INT PRIMARY KEY AUTO_INCREMENT,
            nom VARCHAR(200) NOT NULL,
            url TEXT NOT NULL
            )""")
        
    def creer_table_sous_categories(self) : 
        self.curseur.execute("""CREATE TABLE IF NOT EXISTS sous_categories(
            id INT PRIMARY KEY AUTO_INCREMENT,
            nom VARCHAR(200) NOT NULL,
            url TEXT NOT NULL,
            id_parent INT NOT NULL,
            FOREIGN KEY (id_parent) REFERENCES categorie(id)
            )""")
        
    def creer_table_page_list(self) : 
        self.curseur.execute("""CREATE TABLE IF NOT EXISTS page_list(
            id INT PRIMARY KEY AUTO_INCREMENT,
            nom VARCHAR(200) NOT NULL,
            url TEXT NOT NULL,
            id_parent INT NOT NULL,
            FOREIGN KEY (id_parent) REFERENCES sous_categories(id)
            )""")
        
    def creer_table_produits(self) : 
        self.curseur.execute("""CREATE TABLE IF NOT EXISTS produits(
            id_produit INT PRIMARY KEY,
            nom_produit VARCHAR(250) NOT NULL,
            marque_produit VARCHAR(250),
            prix_produit DOUBLE NOT NULL
            en_promotion BOOL NOT NULL,
            date_fin_promo DATE,
            categorie VARCHAR(250) NOT NULL,
            sous_categorie VARCHAR(250) NOT NULL,
            sous_sous_categorie VARCHAR(250) NOT NULL,
            reference VARCHAR(100),
            code_article VARCHAR(100),
            gencod INT,
            url_produit TEXT NOT NULL
            )""")


    def process_item(self, item, spider):
        return item
    def is_produit_doublon(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter["id_produit"] in self.ids_seen:
            print("ma logique si doublon")
        else:
            self.ids_seen.add(adapter["id_produit"])
            return item
    def insert_produit(self, item, spider):
        adapter = ItemAdapter(item)
        self.curseur.execute(f"""
                    INSERT INTO produits(
                                            id_produit,
                                            nom_produit,
                                            marque_produit,
                                            prix_produit,
                                            en_promotion,
                                            date_fin_promo,
                                            categorie,
                                            sous_categorie,
                                            sous_sous_categorie,
                                            reference,
                                            code_article,
                                            gencod,
                                            url_produit
                                        )
                    VALUES
                        (
                            {adapter['id_produit']},
                            {adapter['nom_produit']},
                            {adapter['marque_produit']},
                            {adapter['prix_produit']},
                            {adapter['en_promotion']},
                            {adapter['date_fin_promo']},
                            {adapter['categorie']},
                            {adapter['sous_categorie']},
                            {adapter['sous_sous_categorie']},
                            {adapter['reference']},
                            {adapter['code_article']},
                            {adapter['gencod']},
                            {adapter['url_produit']}
                        )
                        """
                            )
        
