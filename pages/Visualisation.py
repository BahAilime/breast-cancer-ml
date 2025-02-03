import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Titre de l'application
st.title("Visualisation et Agrégation des Données")

# Chargement des données
@st.cache_data
def load_data():
    data = pd.read_csv("data/breast_cancer.csv")
    return data

df = load_data()

# Afficher un aperçu du dataset si besoin
if st.checkbox("Afficher un aperçu du dataset"):
    st.write(df.head())

st.sidebar.header("Paramètres de Visualisation")

# Presets définis
presets = {
    "Preset 1": {"col_x": "Age", "col_y": "Survival Months", "aggregation": "Moyenne", "graph_type": "Line", "text": "Preset 1"},
}

# Dropdown pour les presets
preset_choice = st.sidebar.selectbox("Choisir un preset", ["Aucun"] + list(presets.keys()))

if preset_choice != "Aucun":
    params = presets[preset_choice]
    col_x = params["col_x"]
    col_y = params["col_y"]
    aggregation = params["aggregation"]
    graph_type = params["graph_type"]
    st.sidebar.markdown(f"### Informations sur le preset sélectionné :")
    st.sidebar.write(f"- **X** : {col_x}")
    st.sidebar.write(f"- **Y** : {col_y}")
    st.sidebar.write(f"- **Agrégation** : {aggregation}")
    st.sidebar.write(f"- **Type de graphique** : {graph_type}")
else:
    # Sélection manuelle
    col_x = st.sidebar.selectbox("Sélectionner la variable X (abscisse)", options=df.columns.tolist())
    col_y = st.sidebar.selectbox("Sélectionner la variable Y (ordonnée)", options=df.columns.tolist())
    aggregation = st.sidebar.selectbox("Choisir le type d'agrégation sur Y", ["Aucune", "Somme", "Moyenne", "Nombre d'occurrences"])
    graph_type = st.sidebar.selectbox("Choisir le type de graphique", ["Scatter", "Line", "Bar"])

st.markdown("---")
st.subheader("Graphique")

def afficher_graphique(df_plot, x, y, graph_type):
    fig, ax = plt.subplots()
    if graph_type == "Scatter":
        ax.scatter(df_plot[x], df_plot[y], alpha=0.7)
    elif graph_type == "Line":
        ax.plot(df_plot[x], df_plot[y])
    elif graph_type == "Bar":
        ax.bar(df_plot[x], df_plot[y])
    ax.set_xlabel(x)
    ax.set_ylabel(y)
    ax.set_title(f"{graph_type} de {y} en fonction de {x}")
    st.pyplot(fig)

if aggregation == "Aucune":
    st.write("Affichage des données brutes")
    afficher_graphique(df, col_x, col_y, graph_type)
else:
    st.write(f"Affichage des données avec agrégation : {aggregation}")
    try:
        if aggregation == "Somme":
            df_agg = df.groupby(col_x)[col_y].sum().reset_index()
        elif aggregation == "Moyenne":
            df_agg = df.groupby(col_x)[col_y].mean().reset_index()
        elif aggregation == "Nombre d'occurrences":
            df_agg = df.groupby(col_x).size().reset_index(name=col_y)
        
        st.write("Données agrégées :", df_agg.head())
        afficher_graphique(df_agg, col_x, col_y, graph_type)
    except Exception as e:
        st.error("Erreur :(", icon="🚨")
        st.error(str(e))

# Affichage du texte explicatif si un preset est sélectionné
if preset_choice != "Aucun":
    st.markdown(presets[preset_choice]["text"], unsafe_allow_html=True)
