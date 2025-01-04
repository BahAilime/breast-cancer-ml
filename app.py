import joblib
import streamlit as st

st.set_page_config(page_title="Prédiction de survie au cancer", page_icon="🏥", layout="wide")
st.title("🏥 Prédiction de survie au cancer du sein")

def make_prediction():
    all_values = [
        age, tstage_value, nstage_value, sixth_stage_value,
        grade_value, a_stage_value, tumor_size,
        int(estrogen), int(progesterone),
        node_examined, node_positive, survival_months
    ]
    
    try:
        model = joblib.load('models/model_rdf.joblib')
        prediction = model.predict_proba([all_values])
        
        with st.session_state.result_placeholder.container():
            st.markdown("### Résultat de la Prédiction")
            if prediction[0][1] > 0.5:
                confidence = f"{prediction[0][1]*100:.1f}%"
                st.success(f"Prédiction: Le patient devrait survivre (Confiance: {confidence})")
            else:
                confidence = f"{prediction[0][0]*100:.1f}%"
                st.error(f"Prédiction: Le patient risque de mourir (Confiance: {confidence})")
            
            with st.expander("Affichez les valeurs de prédiction brutes"):
                st.code(str(prediction))
            
    except NameError:
        with st.session_state.result_placeholder.container():
            st.error("NameError")

col1, col2 = st.columns(2)

with col1:
    tstage = st.radio(
        "T stage",
        options=["T1", "T2", "T3", "T4"],
        index=0,
        horizontal=True,
        on_change=make_prediction
    )
    tstage_value = {"T1": 1, "T2": 2, "T3": 3, "T4": 4}[tstage]

    nstage = st.radio(
        "N stage",
        options=["N1", "N2", "N3"],
        index=0,
        horizontal=True,
        on_change=make_prediction
    )
    nstage_value = {"N1": 1, "N2": 2, "N3": 3}[nstage]
    
    sixth_stage = st.radio(
        "6th stage",
        options=["IIA", "IIB", "IIIA", "IIIB", "IIIC"],
        index=0,
        horizontal=True,
        on_change=make_prediction
    )
    sixth_stage_value = {
        "IIA": 1, "IIB": 2, "IIIA": 3, "IIIB": 4, "IIIC": 5
    }[sixth_stage]
    
    grade = st.radio(
        "Grade",
        options=[
            "Grade I (bien différencié)",
            "Grade II (modérément différencié)",
            "Grade III (peu différencié)",
            "Grade IV (non différencié)"
        ],
        index=0,
        horizontal=True,
        on_change=make_prediction
    )
    grade_options = [
        "Grade I (bien différencié)",
        "Grade II (modérément différencié)",
        "Grade III (peu différencié)",
        "Grade IV (non différencié)"
    ]
    grade_value = {opt: idx + 1 for idx, opt in enumerate(grade_options)}[grade]

    a_stage = st.radio(
        "A stage",
        options=["Regional", "Distant"],
        index=0,
        horizontal=True,
        on_change=make_prediction
    )
    a_stage_value = {"Regional": 1, "Distant": 0}[a_stage]
    
    estrogen = st.checkbox("Recepteurs de l'Estrogen positif", value=True)
    progesterone = st.checkbox("Recepteurs de la Progesterone positif", value=True)

with col2:
    age = st.number_input(
        "Age",
        min_value=1,
        max_value=150,
        value=45,
        on_change=make_prediction
    )
    
    tumor_size = st.number_input(
        "Taille de la tumeur (en mm)",
        min_value=1,
        max_value=200,
        value=27,
        on_change=make_prediction
    )
    
    node_examined = st.slider(
        "Nombre de Noeuds examinés",
        min_value=1,
        max_value=80,
        value=1,
        on_change=make_prediction
    )

    node_positive = st.slider(
        "Nombre de Noeuds positifs",
        min_value=1,
        max_value=80,
        value=1,
        on_change=make_prediction
    )

    survival_months = st.slider(
        "Nombre de mois survécus",
        min_value=1,
        max_value=150,
        value=1,
        on_change=make_prediction
    )
    
if "result_placeholder" not in st.session_state:
    st.session_state.result_placeholder = st.empty()

st.session_state.result_placeholder.container()