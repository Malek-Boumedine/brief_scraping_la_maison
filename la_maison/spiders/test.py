import json
JSON_CATEGORIES = None
with open('categories.json', 'r') as f:
    # Comment: pyfile.txt
    JSON_CATEGORIES = json.load(f)
titre_du_site = JSON_CATEGORIES[0]["titre"]
dict_categories = JSON_CATEGORIES[0]["categories"]
for categorie in dict_categories:
    name_categorie = categorie["nom_cat"]
    for subcategorie in categorie["sous_categories"]:
        print(f"{name_categorie}:{subcategorie["nom_ss_cat"]}")
