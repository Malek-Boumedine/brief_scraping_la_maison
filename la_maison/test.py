import csv

with open("categories.csv", newline="") as fichier:
    donnees = csv.DictReader(fichier, delimiter=",")  
    urls = [row["url"] for row in donnees]  