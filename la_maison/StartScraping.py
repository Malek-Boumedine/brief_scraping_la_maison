import os
import subprocess
import streamlit as st
import time

# Nouvelle variable pour suivre le processus
if "scraping_process" not in st.session_state:
    st.session_state.scraping_process = None
if "scraping_logs" not in st.session_state:
    st.session_state.scraping_logs = []


def execute_command_background(command):
    """Exécute une commande système en arrière-plan et retourne le processus."""
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return process
    except FileNotFoundError:
        st.write(f"Erreur : Commande introuvable : {' '.join(command)}")
        return None
    except Exception as e:
        st.write(f"Erreur inattendue : {e}")
        return None


def start_scraping():
    """Lance le processus de scraping et suit son état."""
    # Supprimer les fichiers obsolètes
    files_to_delete = ["categories.csv"]
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)
            st.write(f"Fichier supprimé : {file}")
        else:
            st.write(f"Fichier introuvable : {file}")

    # Lancer le processus en arrière-plan
    st.write("Exécution de runner_categories.py en arrière-plan...")
    process = execute_command_background(["python3", "runner_categories.py"])
    if process:
        st.session_state.scraping_process = process
        st.session_state.scraping_logs = []
        st.write("Processus de scraping démarré.")
    else:
        st.write("Échec du démarrage du scraping.")


def monitor_scraping():
    """Récupère dynamiquement les logs du processus de scraping."""
    process = st.session_state.scraping_process

    # Conteneur pour afficher les logs avec une hauteur contrainte
    log_container = st.empty()  # Zone où les logs seront affichés

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

    if process and process.poll() is None:  # Vérifie si le processus est actif
        # Lire les logs dynamiquement
        for line in iter(process.stdout.readline, ""):
            if line:  # Ajouter chaque ligne de log
                st.session_state.scraping_logs.append(line.strip())  # Stocker dans l'état

                # Afficher les logs dans le conteneur avec style
                log_container.markdown(
                    f"<div class='log-box'>{'<br>'.join(st.session_state.scraping_logs)}</div>",
                    unsafe_allow_html=True
                )
                time.sleep(0.1)  # Petite pause pour ne pas surcharger l'interface

        # Une fois le processus terminé
        if process.poll() is not None:
            st.session_state.scraping_logs.append("Scraping terminé.")
            log_container.markdown(
                f"<div class='log-box'>{'<br>'.join(st.session_state.scraping_logs)}</div>",
                unsafe_allow_html=True
            )
            st.session_state.scraping_process = None  # Réinitialiser l'état du processus

    elif process and process.poll() is not None:  # Processus terminé mais non monitoré
        st.session_state.scraping_logs.append("Scraping terminé.")
        log_container.markdown(
            f"<div class='log-box'>{'<br>'.join(st.session_state.scraping_logs)}</div>",
            unsafe_allow_html=True
        )
        st.session_state.scraping_process = None  # Réinitialiser l'état du processus


def stop_scraping():
    """Arrête le processus de scraping."""
    process = st.session_state.scraping_process
    if process and process.poll() is None:  # Vérifie si le processus est actif
        process.terminate()  # Envoie un signal pour arrêter le processus proprement
        process.wait()  # Attend la fin du processus
        st.write("Scraping arrêté.")
    else:
        st.write("Aucun processus actif à arrêter.")
    st.session_state.scraping_process = None  # Réinitialise l'état


if __name__ == "__main__":
    # Interface Streamlit
    st.title("Lancement du Scraping")
    st.write("Utilisez les boutons pour démarrer ou arrêter le processus de scraping.")

    if st.button("Démarrer le scraping"):
        if st.session_state.scraping_process is None:
            start_scraping()
        else:
            st.write("Un processus de scraping est déjà en cours.")

    if st.button("Arrêter le scraping"):
        stop_scraping()

    # Affichage des logs dynamiques
    if st.session_state.scraping_process:
        monitor_scraping()

    # Affichage des logs déjà capturés
    st.write("Logs en cours :")
    for log in st.session_state.scraping_logs:
        st.text(log)
