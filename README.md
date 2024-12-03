# 🏠 La Maison - Web Scraping Project

## 📋 Vue d'ensemble

Un outil de scraping robuste développé avec Scrapy pour extraire des données de produits d'un site e-commerce. Le projet est conçu pour parcourir automatiquement des catégories définies et collecter des informations détaillées sur les produits.

## ✨ Fonctionnalités principales

- 🔄 Extraction automatisée des données produits
- 📑 Lecture des catégories depuis un fichier CSV
- 🔍 Collecte détaillée (nom, prix, marque, etc.)
- 📊 Pipeline de traitement des données
- 🚦 Gestion intelligente de la pagination
- insertion dans une base de données
- Application en streamlit qui permet de :
  -  Lancer le scraping des catégories et des produits
  -  Affichage des produits avec différents filtres (catégorie, sous catégorie, promotion ...) et de chercher un produit avec un mot clé.

## 🚀 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/Malek-Boumedine/brief_scraping_la_maison.git
cd la_maison
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

### Prérequis
- Python 3.7+
- Fichier `categories.csv` dans le répertoire racine

### Configuration du Pipeline
```python
ITEM_PIPELINES = {
   'la_maison.pipelines.LaMaisonPipeline': 300,
}
```

## 📦 Structure du projet

```
la_maison/
├── spiders/          # Spiders Scrapy
├── pipelines.py      # Pipelines de traitement
├── settings.py       # Configuration
├── items.py         # Définition des items
└── requirements.txt  # Dépendances
```

## 🎯 Utilisation

Lancer le scraping :
```bash
scrapy crawl spider/spider_categories.py
scrapy crawl spider/spider_produits.py
```
### On peut aussi lancer le runner pour chaque spider

## 📝 Bonnes pratiques

- ⏱️ Configurez des délais entre requêtes
- 🛡️ Implémentez la gestion d'erreurs
- 📊 Validez les données extraites

## 🤝 Contribution

1. Fork du projet
2. Création de branche (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Commit (`git commit -m 'Ajout nouvelle fonctionnalité'`)
4. Push (`git push origin feature/nouvelle-fonctionnalite`)
5. Création d'une Pull Request

## 📚 Documentation

- [Documentation Scrapy](https://docs.scrapy.org/)
- [Guide d'utilisation](./docs/USAGE.md)
- [Guide de contribution](./docs/CONTRIBUTING.md)

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 📧 Contact

Pour toute question : [mon_email@gmail.com](mailto:email@example.com)

---

## 🙏 Remerciements

Merci à tous les contributeurs qui ont participé à l'amélioration de ce projet.
