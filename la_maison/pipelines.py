# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3


class LaMaisonPipeline:
    """
    Classe LaMaisonPipeline pour gérer l'insertion de données dans une base de données SQLite.

    Cette classe établit une connexion à une base de données SQLite et fournit des méthodes pour créer des tables et traiter des éléments. Elle permet d'éviter les doublons lors de l'insertion de produits et gère différentes catégories d'éléments.

    Attributes:
        connexion: La connexion à la base de données SQLite.
        curseur: Le curseur pour exécuter des commandes SQL.
        ids_seen: Un ensemble pour suivre les identifiants de produits déjà vus.

    Methods:
        __init__: Initialise la connexion à la base de données et les attributs.
        creer_tables_categories: Crée la table des catégories si elle n'existe pas.
        creer_table_sous_categories: Crée la table des sous-catégories si elle n'existe pas.
        creer_table_page_list: Crée la table des pages de liste si elle n'existe pas.
        creer_table_produits: Crée la table des produits si elle n'existe pas.
        is_produit_doublon: Vérifie si un produit est un doublon en fonction de son identifiant.
        process_item: Traite un élément en l'insérant dans la base de données selon son type.
    """

    def __init__(self):
        """
        Initialise une instance de LaMaisonPipeline et établit une connexion à la base de données SQLite.

        Cette méthode configure la connexion à la base de données SQLite, initialise un curseur pour exécuter des commandes SQL, 
        et crée un ensemble pour suivre les identifiants de produits déjà vus. Elle appelle également des méthodes pour 
        créer les tables nécessaires dans la base de données.

        Args:
            self: L'instance de la classe.

        Returns:
            None

        Raises:
            sqlite3.Error: Si une erreur se produit lors de l'établissement de la connexion à la base de données.
        """
        
        self.connexion = sqlite3.connect("laMaison.db")
        self.curseur = self.connexion.cursor()
        self.ids_seen = set() 
        self.nombre_doublons = 0
        
        self.creer_tables_categories()
        self.creer_table_sous_categories()
        self.creer_table_page_list()
        self.creer_table_produits()

    def creer_tables_categories(self) -> None : 
        """
        Crée la table des catégories dans la base de données si elle n'existe pas déjà.

        Cette méthode exécute une commande SQL pour créer une table nommée 'categories' avec des colonnes pour l'identifiant, le nom et l'URL. Elle garantit que la table est créée uniquement si elle n'existe pas déjà, évitant ainsi les erreurs lors de l'exécution.

        Args:
            self: L'instance de la classe.

        Returns:
            None
        """

        self.curseur.execute("""CREATE TABLE IF NOT EXISTS categories(
            "id" VARCHAR(20) PRIMARY KEY,
            "nom" VARCHAR(200) NOT NULL,
            "url" TEXT NOT NULL
            )""")

    def creer_table_sous_categories(self) -> None :
        """
        Crée la table des sous-catégories dans la base de données si elle n'existe pas déjà.

        Cette méthode exécute une commande SQL pour créer une table nommée 'sous_categories' avec des colonnes pour l'identifiant, le nom, l'URL et l'identifiant du parent. Elle assure l'intégrité référentielle en définissant une clé étrangère qui référence l'identifiant d'une catégorie.

        Args:
            self: L'instance de la classe.

        Returns:
            None
        """

        self.curseur.execute("""CREATE TABLE IF NOT EXISTS sous_categories(
            "id" VARCHAR(20) PRIMARY KEY,
            "nom" VARCHAR(200) NOT NULL,
            "url" TEXT NOT NULL,
            "id_parent" VARCHAR(20) NOT NULL,
            FOREIGN KEY (id_parent) REFERENCES categorie(id)
            )""")

    def creer_table_page_list(self) -> None :
        """
        Crée la table des pages de liste dans la base de données si elle n'existe pas déjà.

        Cette méthode exécute une commande SQL pour créer une table nommée 'page_list' avec des colonnes pour l'identifiant, le nom, l'URL et l'identifiant du parent. Elle garantit l'intégrité référentielle en définissant une clé étrangère qui référence l'identifiant d'une sous-catégorie.

        Args:
            self: L'instance de la classe.

        Returns:
            None
        """

        self.curseur.execute("""CREATE TABLE IF NOT EXISTS page_list(
            "id" VARCHAR(20) PRIMARY KEY,
            "nom" VARCHAR(200) NOT NULL,
            "url" TEXT NOT NULL,
            "id_parent" VARCHAR(20) NOT NULL,
            FOREIGN KEY (id_parent) REFERENCES sous_categories(id)
            )""")

    def creer_table_produits(self) -> None :
        """
        Crée la table des produits dans la base de données si elle n'existe pas déjà.

        Cette méthode exécute une commande SQL pour créer une table nommée 'produits' avec des colonnes pour l'identifiant du produit, le nom, la marque, le prix, les informations sur les promotions, et d'autres attributs pertinents. Elle assure l'intégrité référentielle en définissant une clé étrangère qui référence l'identifiant d'une page de liste.

        Args:
            self: L'instance de la classe.

        Returns:
            None
        """

        self.curseur.execute("""CREATE TABLE IF NOT EXISTS produits(
            "id_produit" VARCHAR(20) PRIMARY KEY,
            "nom_produit" VARCHAR(250) NOT NULL,
            "marque_produit" INT,
            "prix_produit" DOUBLE NOT NULL,
            "en_promotion" BOOL NOT NULL,
            "date_fin_promo" DATE,
            "id_page_list" VARCHAR(20) NOT NULL,
            "reference" VARCHAR(100),
            "code_article" VARCHAR(100),
            "gencod" INT,
            "url_produit" TEXT NOT NULL,
            FOREIGN KEY (id_page_list) REFERENCES page_list(id)
            )""")

    def is_produit_doublon(self, item, spider) -> dict :
        """
        Vérifie si un produit est un doublon en fonction de son identifiant.

        Cette méthode utilise un adaptateur pour extraire l'identifiant du produit d'un élément donné et détermine si cet identifiant a déjà été vu. Si l'identifiant est un doublon, un message est imprimé et la méthode ne retourne rien ; sinon, l'identifiant est ajouté à l'ensemble des identifiants vus et l'élément est retourné.

        Args:
            self: L'instance de la classe.
            item: L'élément contenant les informations du produit à vérifier.

        Returns:
            L'élément si ce n'est pas un doublon, sinon None.
        """
        
        adapter = ItemAdapter(item)
        if adapter["id_produit"] in self.ids_seen:
            self.nombre_doublons += 1
            print("ma logique si doublon")
        else:
            self.ids_seen.add(adapter["id_produit"])
            return item

    def process_item(self, item, spider) -> dict :
        """
        Traite un élément en l'insérant dans la base de données selon son type.

        Cette méthode gère l'insertion d'éléments dans la base de données SQLite en fonction de leur type. 
        Elle prend en charge les produits, les catégories, les sous-catégories et les pages de liste, 
        tout en évitant les doublons lors de l'insertion.

        Args:
            self: L'instance de la classe.
            item (dict): L'élément à traiter, qui peut contenir des informations sur un produit ou une catégorie. 
            Les clés attendues incluent :
                - "id_produit": Identifiant du produit (pour les produits).
                - "nom_produit": Nom du produit.
                - "marque_produit": Marque du produit.
                - "prix_produit": Prix du produit.
                - "en_promotion": Indicateur de promotion (booléen).
                - "date_fin_promo": Date de fin de promotion.
                - "id_sous_sous_categorie": Identifiant de la sous-sous-catégorie.
                - "reference": Référence du produit.
                - "code_article": Code article du produit.
                - "gencod": Code EAN du produit.
                - "url_produit": URL du produit.
                - "type_cat": Type de l'élément (CAT, S_CAT, PAGE_LIST).
                - "identifiant": Identifiant de la catégorie ou sous-catégorie.
                - "nom_categorie": Nom de la catégorie.
                - "url": URL de la catégorie ou sous-catégorie.
                - "id_parent": Identifiant de la catégorie parente (pour les sous-catégories).

        Returns:
            dict: L'élément traité, tel qu'il a été inséré ou mis à jour dans la base de données.

        Raises:
            sqlite3.Error: Si une erreur se produit lors de l'exécution des commandes SQL.
        """
        
        try :
            
            if "id_produit" in item : 
                if item["id_produit"] not in self.ids_seen:
                    self.curseur.execute("INSERT OR IGNORE INTO produits VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                                    (item["id_produit"], item["nom_produit"], item["marque_produit"], item["prix_produit"], item["en_promotion"], item["date_fin_promo"], item["id_sous_sous_categorie"], item["reference"], item["code_article"], item["gencod"], item["url_produit"]))
                    self.connexion.commit()

            elif item["type_cat"] == "CAT":
                self.curseur.execute("INSERT OR IGNORE INTO categories VALUES(?, ?, ?)",
                                    (item["identifiant"], item["nom_categorie"], item["url"]))
                self.connexion.commit()

            elif item["type_cat"] == "S_CAT":
                self.curseur.execute("INSERT OR IGNORE INTO sous_categories VALUES(?, ?, ?, ?)",
                                    (item["identifiant"], item["nom_categorie"], item["url"], item["id_parent"]))
                self.connexion.commit()

            elif item["type_cat"] == "PAGE_LIST":
                self.curseur.execute("INSERT OR IGNORE INTO page_list VALUES(?, ?,?, ?)",
                                    (item["identifiant"], item["nom_categorie"], item["url"], item["id_parent"]))
                self.connexion.commit()
        
        except sqlite3.Error as e:
            print(f"Une erreur est survenue lors de l'insertion dans la base de données : {e}")

        return item

    def close_spider(self, spider) -> None :
        """
        Méthode appelée automatiquement lors de la fermeture du spider.
        Affiche le nombre total de doublons de produits détectés pendant le scraping.

        Args:
            spider (scrapy.Spider): L'instance du spider qui vient de terminer son exécution.

        Returns:
            None: Cette méthode ne retourne rien, elle affiche uniquement le résultat.
        """
        
        print(f"\nNombre total de doublons trouvés : {self.nombre_doublons}")
        