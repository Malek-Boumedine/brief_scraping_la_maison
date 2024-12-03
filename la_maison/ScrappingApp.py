import streamlit as st
from StartScraping import start_scraping_categories, start_scraping_produit, stop_scraping, monitor_scraping
from ReadBdd import get_table_produit

def run_scraping():
    """
    Affiche les éléments de démarrage et d'arrêt du processus de scraping.
    Permet de gérer le démarrage du scraping des catégories et des produits,
    ainsi que l'arrêt des processus en cours.
    """
    st.title("Lancement du Scraping")
    st.write(
        """
        Utilisez les boutons pour démarrer ou arrêter
        le processus de scraping.
        """
    )

    # Vérification et initialisation de l'état de scraping
    if "scraping_process" not in st.session_state:
        st.session_state.scraping_process = None

    if "scraping_status" not in st.session_state:
        st.session_state.scraping_status = False

    # Boutons de gestion du scraping
    if st.button("Démarrer le scraping Catégorie"):
        if st.session_state.scraping_process is None:
            start_scraping_categories()
        else:
            st.write("Un processus de scraping est déjà en cours.")

    if st.button("Démarrer le scraping Produits"):
        if st.session_state.scraping_process is None:
            start_scraping_produit()
        else:
            st.write("Un processus de scraping est déjà en cours.")

    if st.session_state.scraping_process:
        if st.button("Arrêter le scraping"):
            stop_scraping()
            st.rerun()
        monitor_scraping()

def scraping_on_off(boolean_choice: bool):
    """
    Met à jour l'état du scraping dans le session state sans redémarrer l'interface.

    :param boolean_choice: booléen indiquant si le scraping est activé ou désactivé
    """
    st.session_state.scraping_status = boolean_choice

def switch_interface(interface: str):
    """
    Change l'interface affichée en mettant à jour l'état focus_interface.

    :param interface: Nom de l'interface à afficher
    """
    if st.session_state.scraping_process is None:
        st.session_state.focus_interface = interface
        st.rerun()
    else:
        st.write("Un processus de scraping est en cours. Veuillez l'arrêter ou attendre sa fin avant de changer d'interface.")

def switch_accueil():
    """Bascule vers l'interface d'accueil."""
    switch_interface("accueil")

def switch_categorie():
    """Bascule vers l'interface de gestion des catégories."""
    switch_interface("categorie")

def switch_produit():
    """Bascule vers l'interface de gestion des produits."""
    switch_interface("produit")

def switch_general_database():
    """Bascule vers l'interface de visualisation de la base de données complète."""
    switch_interface("toute_la_data_base")

def button_run_scraping(name_button: str = "Start_Scraping"):
    """
    Affiche un bouton pour démarrer le scraping.

    :param name_button: Texte affiché sur le bouton
    """
    if st.button(label=name_button):
        scraping_on_off(True)

def button_stop_scraping(name_button: str = "Stop_Scraping"):
    """
    Affiche un bouton pour arrêter le scraping.

    :param name_button: Texte affiché sur le bouton
    """
    if st.button(label=name_button):
        scraping_on_off(False)

def button_switch_produit(name_button: str = "View_Produit"):
    """
    Affiche un bouton pour basculer vers l'interface produit.

    :param name_button: Texte affiché sur le bouton
    """
    if st.button(label=name_button):
        st.write("View Produit")

def button_switch_categorie(name_button: str = "View_Categorie"):
    """
    Affiche un bouton pour basculer vers l'interface catégorie.

    :param name_button: Texte affiché sur le bouton
    """
    if st.button(label=name_button):
        switch_categorie()

def button_switch_general_database(name_button: str = "VoirTout"):
    """
    Affiche un bouton pour basculer vers la visualisation complète de la base de données.

    :param name_button: Texte affiché sur le bouton
    """
    if st.button(label=name_button):
        switch_general_database()

def button_switch_accueil(name_button: str = "Accueil"):
    """
    Affiche un bouton pour retourner à l'accueil.

    :param name_button: Texte affiché sur le bouton
    """
    if st.button(label=name_button):
        switch_accueil()

def interface_acceuil():
    """Affiche l'interface d'accueil avec les options de scraping et de navigation."""
    st.write("Bienvenue !")
    button_switch_general_database()
    run_scraping()

def interface_data_base():
    """Affiche l'interface de visualisation de la base de données."""
    get_table_produit()
    button_switch_accueil()

def interface():
    """
    Gère l'affichage dynamique des interfaces selon le contexte défini dans session_state.
    Permet de basculer entre différentes interfaces comme l'accueil ou la base de données.
    """
    if "focus_interface" not in st.session_state:
        st.session_state.focus_interface = "accueil"

    focus = st.session_state.focus_interface
    interface_choice = {
        "accueil": interface_acceuil,
        "toute_la_data_base": interface_data_base
    }

    if focus in interface_choice:
        interface_choice[focus]()
    else:
        st.error("Oups, vous vous êtes perdu dans les limbes.")
        if st.button("Retour à l'Accueil"):
            switch_interface("accueil")

if __name__ == "__main__":
    interface()
