import streamlit as st
import sqlite3
import pandas as pd

# Titre de l'application



def get_table(name_table,name_database="laMaison.db"):
    # Charger les données dans un DataFrame
    # Connexion à la base de données SQLite
    la_maison_db = sqlite3.connect(name_database)
    query = f"SELECT * FROM {name_table}"
    df = pd.read_sql_query(query, la_maison_db)
    la_maison_db.close()
    return df
def get_table_produit():
    df = get_table("produits")
    # Afficher le DataFrame dans Streamlit
    if not df.empty:
        st.subheader("Données de la table Produits :")
        st.dataframe(df)  # Affiche un tableau interactif
    else:
        st.warning("La table 'produits' est vide ou n'existe pas.")

def get_table_categories():
    df = get_table("categories")
    # Afficher le DataFrame dans Streamlit
    if not df.empty:
        st.subheader("Données de la table Categories:")
        st.dataframe(df)  # Affiche un tableau interactif
    else:
        st.warning("La table 'categories' est vide ou n'existe pas.")

def get_table_page_list():
    df = get_table("page_list")
    # Afficher le DataFrame dans Streamlit
    if not df.empty:
        st.subheader("Données de la table Page_list:")
        st.dataframe(df)  # Affiche un tableau interactif
    else:
        st.warning("La table 'page list' est vide ou n'existe pas.")


def get_table_sous_categories():
    df = get_table("sous_categories")
    # Afficher le DataFrame dans Streamlit
    if not df.empty:
        st.subheader("Données de la table Sous categories:")
        st.dataframe(df)  # Affiche un tableau interactif
    else:
        st.warning("La table 'Sous_categories' est vide ou n'existe pas.")


if __name__ == "__main__":
    st.title("Affichage des données de la table Produits")
    get_table_produit()
    st.title("Affichage des données de la table Categories")
    get_table_categories()
    st.title("Affichage des données de la table sous_categories")
    get_table_sous_categories()
    st.title("Affichage des données de la table page list")
    get_table_page_list()