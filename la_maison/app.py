import streamlit as st
import sqlite3
import pandas as pd
from typing import Optional



def connecter_bdd():
    """
    Établit une connexion à la base de données SQLite.

    Returns:
        sqlite3.Connection: Objet de connexion à la base de données
    """
    return sqlite3.connect('laMaison.db')


@st.cache_data(ttl=3600)  # Cache pendant 1 heure - système de cache pour les requêtes fréquentes
def charger_categories():
    """
    Charge les catégories depuis la base de données.

    Returns:
        tuple: (categories, sous_categories, liste_pages) DataFrames
    """
    conn = connecter_bdd()
    categories = pd.read_sql_query("SELECT * FROM categories", conn)
    sous_categories = pd.read_sql_query("SELECT * FROM sous_categories", conn)
    liste_pages = pd.read_sql_query("SELECT * FROM page_list", conn)
    conn.close()
    return categories, sous_categories, liste_pages


def charger_promotions(recherche: Optional[str] = None):
    """
    Charge les produits en promotion avec option de recherche.

    Args:
        recherche: Terme de recherche optionnel

    Returns:
        pd.DataFrame: DataFrame contenant les produits en promotion filtrés
    """
    conn = connecter_bdd()
    requete = """
    SELECT DISTINCT p.*,
           c.nom as categorie_nom,
           sc.nom as sous_categorie_nom,
           pl.nom as page_list_nom
    FROM produits p
    LEFT JOIN page_list pl ON p.id_page_list = pl.id
    LEFT JOIN sous_categories sc ON pl.id_parent = sc.id
    LEFT JOIN categories c ON sc.id_parent = c.id
    WHERE p.en_promotion = 1
    """

    parametres = []
    if recherche:
        requete += """ AND (
            p.nom_produit LIKE ?
            OR p.marque_produit LIKE ?
            OR p.reference LIKE ?
            OR p.code_article LIKE ?
            OR CAST(p.prix_produit AS TEXT) LIKE ?
        )"""
        motif_recherche = f"%{recherche}%"
        parametres.extend([motif_recherche] * 5)

    promos = pd.read_sql_query(requete, conn, params=parametres)
    conn.close()
    return promos


def charger_produits(id_categorie: Optional[str] = None, 
                    id_sous_categorie: Optional[str] = None, 
                    id_page_liste: Optional[str] = None,
                    recherche: Optional[str] = None) -> pd.DataFrame:
    """
    Charge les produits selon les filtres sélectionnés.

    Args:
        id_categorie: ID de la catégorie
        id_sous_categorie: ID de la sous-catégorie
        id_page_liste: ID de la page_list
        recherche: Terme de recherche

    Returns:
        pd.DataFrame: DataFrame contenant les produits filtrés
    """
    conn = connecter_bdd()

    requete = """
    SELECT DISTINCT p.*,
           c.nom as nom_categorie,
           sc.nom as nom_sous_categorie,
           pl.nom as nom_page_liste
    FROM produits p
    LEFT JOIN page_list pl ON p.id_page_list = pl.id
    LEFT JOIN sous_categories sc ON pl.id_parent = sc.id
    LEFT JOIN categories c ON sc.id_parent = c.id
    WHERE 1=1
    """
    parametres = []

    if id_page_liste:
        requete += " AND p.id_page_list = ?"
        parametres.append(id_page_liste)
    elif id_sous_categorie:
        requete += " AND pl.id_parent = ?"
        parametres.append(id_sous_categorie)
    elif id_categorie:
        requete += " AND sc.id_parent = ?"
        parametres.append(id_categorie)

    if recherche:
        requete += """ AND (
            p.nom_produit LIKE ?
            OR p.marque_produit LIKE ?
            OR p.reference LIKE ?
            OR p.code_article LIKE ?
            OR CAST(p.prix_produit AS TEXT) LIKE ?
        )"""
        motif_recherche = f"%{recherche}%"
        parametres.extend([motif_recherche] * 5)

    produits = pd.read_sql_query(requete, conn, params=parametres)
    conn.close()
    return produits


def main():
    st.title("La Maison - Catalogue de Produits")

    # Bouton de réinitialisation
    col_reset, col_empty = st.columns([1, 4])  # Pour aligner le bouton à gauche
    with col_reset:
        if st.button("🔄 Réinitialiser les filtres"):
            # Réinitialiser tous les états
            st.session_state.numero_page = 1
            if 'terme_recherche' in st.session_state:
                del st.session_state.terme_recherche
            st.rerun()
            
    # Charger les données dès le début
    categories, sous_categories, liste_pages = charger_categories()

    # Bouton Promotions en haut de la page
    afficher_promos = st.toggle('🏷️ Afficher uniquement les promotions', help="Affiche tous les produits en promotion")
    st.write("🔍 **Recherche :** Entrez un ou plusieurs mots-clés (ex: 'Perceuse')")
    terme_recherche = st.text_input("Rechercher un produit", help="La recherche trouvera les produits contenant tous les mots-clés")
    
    if afficher_promos:
        # Afficher uniquement les promotions
        df_produits = charger_promotions(recherche=terme_recherche)
        st.write("### 🏷️ Produits en promotion")
        
    # Colonnes pour les filtres
    if not afficher_promos:
        col1, col2, col3 = st.columns(3)

        with col1:
            # Option "Tous" ajoutée à la liste des catégories
            options_categories = ["Tous"] + categories['id'].tolist()
            categorie_selectionnee = st.selectbox(
                "Catégorie",
                options=options_categories,
                format_func=lambda x: "Toutes les catégories" if x == "Tous" 
                else categories[categories['id'] == x]['nom'].iloc[0]
            )

        with col2:
            if categorie_selectionnee and categorie_selectionnee != "Tous":
                sous_cats_filtrees = sous_categories[
                    sous_categories['id_parent'] == categorie_selectionnee
                ]
                options_sous_cats = ["Tous"] + sous_cats_filtrees['id'].tolist()
                sous_categorie_selectionnee = st.selectbox(
                    "Sous-catégorie",
                    options=options_sous_cats,
                    format_func=lambda x: "Toutes les sous-catégories" if x == "Tous"
                    else sous_cats_filtrees[sous_cats_filtrees['id'] == x]['nom'].iloc[0]
                )
            else:
                sous_categorie_selectionnee = None
                st.selectbox("Sous-catégorie", ["Toutes les sous-catégories"], disabled=True)

        with col3:
            if sous_categorie_selectionnee and sous_categorie_selectionnee != "Tous":
                pages_filtrees = liste_pages[
                    liste_pages['id_parent'] == sous_categorie_selectionnee
                ]
                options_pages = ["Tous"] + pages_filtrees['id'].tolist()
                page_selectionnee = st.selectbox(
                    "Page",
                    options=options_pages,
                    format_func=lambda x: "Toutes les pages" if x == "Tous"
                    else pages_filtrees[pages_filtrees['id'] == x]['nom'].iloc[0]
                )
            else:
                page_selectionnee = None
                st.selectbox("Page", ["Toutes les pages"], disabled=True)

        # Charger les produits selon les filtres
        id_cat = None if categorie_selectionnee == "Tous" else categorie_selectionnee
        id_sous_cat = None if not sous_categorie_selectionnee or sous_categorie_selectionnee == "Tous" else sous_categorie_selectionnee
        id_page = None if not page_selectionnee or page_selectionnee == "Tous" else page_selectionnee

        df_produits = charger_produits(
            id_categorie=id_cat,
            id_sous_categorie=id_sous_cat,
            id_page_liste=id_page,
            recherche=terme_recherche
        )

    tri_options = ['Prix croissant', 'Prix décroissant', 'Nom A-Z', 'Nom Z-A']
    tri_choisi = st.selectbox("Trier par:", tri_options)

    if tri_choisi == 'Prix croissant':
        df_produits = df_produits.sort_values('prix_produit')
    elif tri_choisi == 'Prix décroissant':
        df_produits = df_produits.sort_values('prix_produit', ascending=False)
    elif tri_choisi == 'Nom A-Z':
        df_produits = df_produits.sort_values('nom_produit')
    elif tri_choisi == 'Nom Z-A':
        df_produits = df_produits.sort_values('nom_produit', ascending=False)

    # Paramètres de pagination
    produits_par_page = st.select_slider(
        "Produits par page",
        options=[10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        value=20
    )

    # Pagination
    nombre_pages = len(df_produits) // produits_par_page + (1 if len(df_produits) % produits_par_page > 0 else 0)

    # Stocker le numéro de page
    if 'numero_page' not in st.session_state:
        st.session_state.numero_page = 1

    # Boutons de navigation
    col_prec, col_info, col_suiv = st.columns([1, 2, 1])

    with col_prec:
        if st.button('← Page précédente') and st.session_state.numero_page > 1:
            st.session_state.numero_page -= 1
            st.rerun()

    with col_info:
        st.write(f"Page {st.session_state.numero_page} sur {nombre_pages}")

    with col_suiv:
        if st.button('Page suivante →') and st.session_state.numero_page < nombre_pages:
            st.session_state.numero_page += 1
            st.rerun()

    if nombre_pages > 0:
        debut_idx = (st.session_state.numero_page - 1) * produits_par_page
        fin_idx = debut_idx + produits_par_page
        produits_page = df_produits.iloc[debut_idx:fin_idx]
    else:
        produits_page = df_produits

    
    # Affichage des résultats
    st.write(f"Nombre total de produits trouvés : {len(df_produits)}")

    for _, produit in produits_page.iterrows():
        with st.expander(f"{produit['nom_produit']} - {produit['prix_produit']}€"):
            cols = st.columns(2)
            with cols[0]:
                st.write("**Informations produit:**")
                st.write(f"ID: {produit['id_produit']}")
                st.write(f"Marque: {produit['marque_produit']}")
                st.write(f"Référence: {produit['reference']}")
                st.write(f"Code article: {produit['code_article']}")
            with cols[1]:
                st.write("**Catégorisation:**")
                # Vérification de l'existence des colonnes avant affichage
                if 'categorie_nom' in produit:
                    st.write(f"Catégorie: {produit['categorie_nom']}")
                elif 'nom_categorie' in produit:
                    st.write(f"Catégorie: {produit['nom_categorie']}")

                if 'sous_categorie_nom' in produit:
                    st.write(f"Sous-catégorie: {produit['sous_categorie_nom']}")
                elif 'nom_sous_categorie' in produit:
                    st.write(f"Sous-catégorie: {produit['nom_sous_categorie']}")

                if 'page_list_nom' in produit:
                    st.write(f"Page: {produit['page_list_nom']}")
                elif 'nom_page_liste' in produit:
                    st.write(f"Page: {produit['nom_page_liste']}")

            if produit['en_promotion']:
                st.write("🏷️ **En promotion** jusqu'au:", produit['date_fin_promo'])

            st.write("**Lien produit:**")
            st.write(produit['url_produit'])

if __name__ == "__main__":
    main()