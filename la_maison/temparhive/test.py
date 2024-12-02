import json
JSON_CATEGORIES = None
with open('categories.json', 'r') as f:
    JSON_CATEGORIES = json.load(f)

liste_urls = []
for objet in JSON_CATEGORIES : 
    liste_urls.append(objet["url"])
    
print(len(liste_urls))

print(liste_urls[0])
