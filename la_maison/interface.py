import streamlit as st
from StartScraping import start_scraping, stop_scraping, monitor_scraping


def run_scraping():
    """Affiche les éléments de démarrage et d'arrêt du scraping"""
    st.title("Lancement du Scraping")
    st.write("""
             Utilisez les boutons pour démarrer ou arrêter
             le processus de scraping.""")

    # Vérification de l'état de scraping, initialisation si non défini
    if "scraping_process" not in st.session_state:
        st.session_state.scraping_process = None  # Valeur par défaut pour scraping_process

    if "scraping_status" not in st.session_state:
        st.session_state.scraping_status = False  # Valeur par défaut pour scraping_status

    if st.button("Démarrer le scraping"):
        if st.session_state.scraping_process is None:
            start_scraping()
            # Affichage des logs dynamiques du scraping
        else:
            st.write("Un processus de scraping est déjà en cours.")
    if st.session_state.scraping_process:
        if st.button("Arrêter le scraping"):
            stop_scraping()
            st.rerun()
        monitor_scraping()





def scraping_on_off(boolean_choice: bool):
    """Met à jour l'état du scraping sans redémarrer l'interface"""
    st.session_state.scraping_status = boolean_choice

def switch_interface(interface: str):
    """Change l'interface sans redémarrer toute l'application"""
    st.session_state.focus_interface = interface

def switch_accueil():
    switch_interface("accueil")

def switch_categorie():
    switch_interface("categorie")

def switch_produit():
    switch_interface("produit")

def switch_general_database():
    switch_interface("toute_la_data_base")

def button_run_scraping(name_button: str = "Start_Scraping"):
    """Affiche un bouton de démarrage du scraping"""
    if st.button(label=name_button):
        scraping_on_off(True)

def button_stop_scraping(name_button: str = "Stop_Scraping"):
    """Affiche un bouton d'arrêt du scraping"""
    if st.button(label=name_button):
        scraping_on_off(False)

def button_switch_produit(name_button: str = "View_Produit"):
    """Affiche un bouton de vue produit"""
    if st.button(label=name_button):
        st.write("View Produit")

def button_switch_categorie(name_button: str = "View_Categorie"):
    """Affiche un bouton de vue catégorie"""
    if st.button(label=name_button):
        switch_categorie()

def button_switch_general_database(name_button: str = "VoirTout"):
    """Affiche un bouton pour basculer vers la base de données"""
    if st.button(label=name_button):
        switch_general_database()

def button_switch_accueil(name_button: str = "Accueil"):
    """Affiche un bouton de retour à l'accueil"""
    if st.button(label=name_button):
        switch_accueil()

def interface_acceuil():
    """Affiche l'interface d'accueil avec les options de scraping"""
    st.write("Bienvenue !")
    button_switch_general_database()
    run_scraping()

def interface_data_base():
    """Affiche l'interface pour la base de données"""
    st.write("Ici la future base de données")
    button_switch_accueil()

def interface():
    """Gère l'affichage dynamique des interfaces"""
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
        st.error("Oups, vous vous êtes perdu dans les lymbes.")
        if st.button("Retour à l'Accueil"):
            switch_interface("accueil")

if __name__ == "__main__":
    interface()
