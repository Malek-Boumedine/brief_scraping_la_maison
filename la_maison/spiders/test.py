import re

# Chaîne contenant les attributs du produit
attributs_produit = "Référence : DTM51ZJX3 / Code article : 0398277"

# Expressions régulières pour extraire la référence et le code article
regex_reference = r"Référence\s*:\s*(\S+)"
regex_code_article = r"Code article\s*:\s*(\S+)"

# Recherche de la référence
match_reference = re.search(regex_reference, attributs_produit)
reference = match_reference.group(1) if match_reference else None

# Recherche du code article
match_code_article = re.search(regex_code_article, attributs_produit)
code_article = match_code_article.group(1) if match_code_article else None

# Affichage des résultats
print(f"Référence : {reference}")
print(f"Code article : {code_article}")