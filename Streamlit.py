import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Chemin local vers le fichier Excel
local_file_path = "donnees_imputees_knn_mondial.xlsx"

# Fonction pour charger les données des feuilles Excel en DataFrames
@st.cache_data
def load_excel_data():
    try:
        sheets = pd.read_excel(local_file_path, sheet_name=None)
        # Normaliser les noms de colonnes
        for key in sheets.keys():
            sheets[key].columns = [col.strip().lower() for col in sheets[key].columns]
        return sheets
    except FileNotFoundError:
        st.error(f"Le fichier '{local_file_path}' est introuvable.")
        return None
    except Exception as e:
        st.error(f"Erreur lors du chargement : {str(e)}")
        return None

# Charger les données
excel_data = load_excel_data()

if excel_data:
    st.write("Chargement réussi!")

    # Sélectionner le premier pays
    country1 = st.selectbox("Sélectionner le premier pays", list(excel_data.keys()))
    df1 = excel_data[country1]

    # Exclure la colonne 'date' des indicateurs
    indicators1 = [col for col in df1.columns if col != 'date']

    # Sélectionner un indicateur à afficher pour le premier pays
    indicator1 = st.selectbox("Sélectionner un indicateur pour le premier pays", indicators1)

    # Sélectionner le deuxième pays
    country2 = st.selectbox("Sélectionner le deuxième pays", list(excel_data.keys()), index=1)
    df2 = excel_data[country2]

    # Exclure la colonne 'date' des indicateurs
    indicators2 = [col for col in df2.columns if col != 'date']

    # Sélectionner un indicateur à afficher pour le deuxième pays
    indicator2 = st.selectbox("Sélectionner un indicateur pour le deuxième pays", indicators2)

    # Créer une courbe d'évolution de l'indicateur pour les deux pays
    fig, ax = plt.subplots()
    ax.plot(df1['date'], df1[indicator1], marker='o', linestyle='-', color='b', label=f"{country1} - {indicator1}")
    ax.plot(df2['date'], df2[indicator2], marker='o', linestyle='-', color='r', label=f"{country2} - {indicator2}")
    
    ax.set_title(f"Comparaison de l'évolution des indicateurs")
    ax.set_xlabel("Date")
    ax.set_ylabel("Valeur")
    ax.grid(True)
    ax.legend()

    # Afficher la courbe
    st.pyplot(fig)
else:
    st.stop()  # Stopper l'exécution en cas d'erreur
