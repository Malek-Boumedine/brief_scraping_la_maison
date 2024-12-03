# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    """
    Représente un produit dans le cadre du scraping de données.

    Cette classe hérite de scrapy.Item et définit les champs qui seront utilisés pour stocker les informations
    relatives à un produit extrait d'un site web. Chaque champ correspond à une caractéristique du produit
    et est défini comme un champ Scrapy.

    Attributs:
        id_produit (str): Identifiant unique du produit.
        nom_produit (str): Nom du produit.
        marque_produit (str): Marque du produit.
        prix_produit (float): Prix du produit.
        en_promotion (bool): Indicateur de promotion (True si le produit est en promotion, False sinon).
        date_fin_promo (str): Date de fin de promotion au format 'YYYY-MM-DD'.
        categorie (str): Nom de la catégorie à laquelle appartient le produit.
        sous_categorie (str): Nom de la sous-catégorie à laquelle appartient le produit.
        sous_sous_categorie (str): Nom de la sous-sous-catégorie à laquelle appartient le produit.
        id_sous_sous_categorie (str): Identifiant de la sous-sous-catégorie.
        reference (str): Référence du produit.
        code_article (str): Code article du produit.
        gencod (str): Code EAN (European Article Number) du produit.
        url_produit (str): URL du produit sur le site web.
    """
    
    id_produit = scrapy.Field()
    nom_produit = scrapy.Field()
    marque_produit = scrapy.Field()
    prix_produit = scrapy.Field()
    en_promotion = scrapy.Field()
    date_fin_promo = scrapy.Field()
    categorie = scrapy.Field()
    sous_categorie = scrapy.Field()
    sous_sous_categorie = scrapy.Field()
    id_sous_sous_categorie = scrapy.Field()
    reference = scrapy.Field()
    code_article = scrapy.Field()
    gencod = scrapy.Field()
    url_produit = scrapy.Field()


class categorieItem(scrapy.Item):
    """
    Représente une catégorie dans le cadre du scraping de données.

    Cette classe hérite de scrapy.Item et définit les champs qui seront utilisés pour stocker les informations
    relatives à une catégorie extraite d'un site web. Chaque champ correspond à une caractéristique de la catégorie
    et est défini comme un champ Scrapy.

    Attributs:
        identifiant (int): Identifiant unique de la catégorie.
        nom_categorie (str): Nom de la catégorie.
        type_cat (str): Type de la catégorie (par exemple, "CAT" pour catégorie principale, "S_CAT" pour sous-catégorie).
        url (str): URL de la catégorie sur le site web.
        id_parent (str): Identifiant de la catégorie parente, si applicable (None si la catégorie n'a pas de parent).
    """
    
    identifiant = scrapy.Field()
    nom_categorie = scrapy.Field()
    type_cat = scrapy.Field()
    url = scrapy.Field()
    id_parent = scrapy.Field()


