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
        self.curseur.execute("""CREATE TABLE IF NOT EXISTS page_list(
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
