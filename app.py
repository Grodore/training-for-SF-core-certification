import streamlit as st
import pandas as pd
import random

def select_random_elements_from_list(number_of_selection, liste):
    if number_of_selection > len(liste):
        return "Error: More elements requested than are available in the list."
    return random.sample(liste, number_of_selection)

def extraction_des_reponses(chaine):
    cadre = "[]\"'"
    liste = []
    for i in cadre:
        chaine = chaine.replace(i, "")
    liste = chaine.split(',')
    return [item.strip() for item in liste]

def fetch_data(session, number_of_rows_to_fetch=10):
    lenmax = 50
    random_ids = random.sample(range(1, lenmax + 1), number_of_rows_to_fetch)
    id_list = ', '.join(map(str, random_ids))
    query = f"SELECT * FROM SF_CORE_CERTIFICATION_TRAINING.TRAINING_DATA.QUESTIONS WHERE ID IN ({id_list})"
    df = session.sql(query).to_pandas()
    return df

st.title("Application d'entrainement pour la certification Snowflake Core")

nombre_de_question =st.selectbox("Nombre de questions", list(range(1,50)))

cnx = st.connection("snowflake")
session = cnx.session()

if 'df' not in st.session_state:
    st.session_state.df = fetch_data(session, nombre_de_question)

if 'mode' not in st.session_state:
    st.session_state.mode = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'checked_answers' not in st.session_state:
    st.session_state.checked_answers = {}

if st.button("Mode examen, score et correction à la fin"):
    st.session_state.mode = 1
    st.write("Mode examen sélectionné !")
if st.button("Mode entrainement, correction à chaque question"):
    st.session_state.mode = 2
    st.write("Mode entrainement sélectionné !")

if st.session_state.mode == 1:
    for index, row in enumerate(st.session_state.df.itertuples()):
        st.subheader(f"Question {index + 1}")
        st.write(row.ENONCE)
        rep_list = extraction_des_reponses(row.REPONSES)
        corrections = extraction_des_reponses(row.CORRECTION)
        user_checks = []
        for i, r in enumerate(rep_list):
            key = f"check-{index}-{i}"
            if st.checkbox(r, key=key, value=st.session_state.checked_answers.get(key, False)):
                user_checks.append(r)
                st.session_state.checked_answers[key] = True
            else:
                st.session_state.checked_answers[key] = False
        if set(user_checks) == set(corrections):
            st.session_state.score += 1
    if st.button("Afficher le score final"):
        st.write("Score final :", st.session_state.score)
st.session_state.score = 0
