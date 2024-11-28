import csv
def search_id_produit():
    with open("produits.csv", newline="") as fichier:
        donnees = csv.DictReader(fichier, delimiter=",")  
        return [int(row["id_produit "]) for row in donnees]
product_id_list = search_id_produit()
product_id_list.sort()
is_unique = True
len_product_id = len(product_id_list)
for i in range(len_product_id-1):
    if product_id_list[i] == product_id_list[i+1]:
        is_unique = False
        print(f"{product_id_list[i]=} valeur identique {product_id_list[i+1]}")
        break
if is_unique:
    print("aucun doublon repérer")