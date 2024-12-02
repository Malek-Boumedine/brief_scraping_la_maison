
import os
import subprocess
import streamlit as st
import time

if "scraping_process" not in st.session_state:
    st.session_state.scraping_process = None
if "scraping_logs" not in st.session_state:
    st.session_state.scraping_logs = []
if "scraping_stage" not in st.session_state:
    st.session_state.scraping_stage = None

def execute_command_background(command):
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return process
    except FileNotFoundError:
        st.write(f"Erreur : Commande introuvable : {' '.join(command)}")
        return None
    except Exception as e:
        st.write(f"Erreur inattendue : {e}")
        return None

def add_log(log_line):
    st.session_state.scraping_logs.append(log_line)
    if len(st.session_state.scraping_logs) > 100:
        st.session_state.scraping_logs.pop(0)

def start_scraping_categories():
    files_to_delete = ["categories.csv", "produits.csv", "laMaison.db"]
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            st.write(f"Fichier supprimé : {file}")
        else:
            st.write(f"Fichier introuvable : {file}")

    st.session_state.scraping_stage = "categories"
    st.write("Exécution de runner_categories.py en arrière-plan...")
    process = execute_command_background(["python3", "runner_categories.py"])
    if process:
        st.session_state.scraping_process = process
        st.session_state.scraping_logs = []
        st.write("Processus de scraping pour 'categories' démarré.")
    else:
        st.write("Échec du démarrage du scraping pour 'categories'.")

def start_scraping_produit():
    st.session_state.scraping_stage = "produits"
    st.write("Exécution de runner_produits.py en arrière-plan...")
    process = execute_command_background(["python3", "runner_produits.py"])
    if process:
        st.session_state.scraping_process = process
        st.session_state.scraping_logs = []
        st.write("Processus de scraping pour 'produits' démarré.")
    else:
        st.write("Échec du démarrage du scraping pour 'produits'.")

def monitor_scraping():
    process = st.session_state.scraping_process
    log_container = st.empty()
    
    log_styles = """
        <style>
        .log-box {
            height: 300px; /* Limite la hauteur */
            overflow-y: auto; /* Active le scroll vertical */
            background-color: black; /* Couleur de fond */
            color: green; /* Couleur de texte des vrais hacker :') */
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
            font-family: monospace; /* Style typique pour les logs */
            white-space: pre-wrap; /* Préserve les sauts de ligne */
        }
        </style>
    """
    st.markdown(log_styles, unsafe_allow_html=True)  # Injection des styles

    if process and process.poll() is None:
        for line in iter(process.stdout.readline, ""):
            if line:
                add_log(line.strip())
                log_container.markdown(f"<div class='log-box'>{'<br>'.join(st.session_state.scraping_logs)}</div>", unsafe_allow_html=True)
        time.sleep(0.5)

def stop_scraping():
    process = st.session_state.scraping_process
    if process and process.poll() is None:
        try:
            process.terminate()
            process.wait(timeout=5)
            st.write("Scraping arrêté.")
        except subprocess.TimeoutExpired:
            st.write("Le processus a mis trop de temps à se terminer, forçage de l'arrêt.")
            process.kill()
        except Exception as e:
            st.write(f"Erreur lors de l'arrêt du processus : {e}")
    else:
        st.write("Aucun processus actif à arrêter.")

    st.session_state.scraping_process = None

if __name__ == "__main__":
    st.title("Lancement du Scraping")
    st.write("Utilisez les boutons pour démarrer ou arrêter le processus de scraping.")

    if st.button("Démarrer le scraping"):
        if st.session_state.scraping_process is None:
            start_scraping_categories()
        else:
            st.write("Un processus de scraping est déjà en cours.")

    if st.button("Arrêter le scraping"):
        stop_scraping()

    if st.session_state.scraping_process:
        monitor_scraping()

    st.write("Logs en cours :")
    for log in st.session_state.scraping_logs:
        st.text(log)
