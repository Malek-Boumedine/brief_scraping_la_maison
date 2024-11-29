import streamlit as st

def switch_interface(interface:str):
    st.session_state.focus_interface = interface
    st.rerun()
def switch_accueil():
    switch_interface("accueil")
def switch_categorie():
    switch_interface("categorie")
def switch_produit():
    switch_interface("produit")
def switch_general_database():
    switch_interface("toute_la_data_base")

def button_scraping(name_button: str="Start_Scraping"):
    if st.button(label=name_button):
        st.write("Run Scraping...")
def button_switch_produit(name_button: str="View_Produit"):
    if st.button(label=name_button):
        st.write("View Produit")
def button_switch_categorie(name_button: str="View_Categorie"):
    if st.button(label=name_button):
        switch_categorie()
def button_switch_general_database(name_button:str="VoirTout"):
    if st.button(label=name_button):
        switch_general_database()
def button_switch_accueil(name_button: str="Accueil"):
    if st.button(label=name_button):
        switch_accueil()



def interface_acceuil():
    st.write("Bienvenue !")
    button_switch_general_database()
def interface_data_base():
    st.write("Ici la future base de donnee")
    button_switch_accueil()

def interface():
    if "focus_interface" not in  st.session_state:
        st.session_state.focus_interface = "accueil"
        st.rerun()
    focus = st.session_state.focus_interface
    interface_choice = {
                        "accueil": interface_acceuil,
                        "toute_la_data_base": interface_data_base
                        }
    if focus in interface_choice:
        interface_choice[focus]()
    else:
        st.error("Oups vous vous êtes perdu dans les lymbes")
        if st.button("Retour à l'Accueil"):
            switch_interface("default")
    
        
if __name__ == "__main__":
    interface()