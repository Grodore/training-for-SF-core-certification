import streamlit as st
import pandas as pd
import random

# Function Definitions

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

# Display the select box and get user input
nombre_de_question = st.selectbox("Nombre de questions", list(range(1, 51)))




if 'mode' not in st.session_state:
    st.session_state.mode = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'checked_answers' not in st.session_state:
    st.session_state.checked_answers = {}
if 'df' not in st.session_state:
    st.session_state.df = None
# Button to fetch or refresh data
if st.button("Fetch Data"):
    cnx = st.connection("snowflake")
    session = cnx.session()
    st.session_state.df = fetch_data(session, nombre_de_question)

# Check if the DataFrame is loaded
if 'df' in st.session_state:
    # Exam modes and question display logic...

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
            user_checks = []
            corrections = []
            rep_list = extraction_des_reponses(row.REPONSES)
            corrections = extraction_des_reponses(row.CORRECTION)
            
            for i, r in enumerate(rep_list):
                key = f"check-{index}-{i}"
                if st.checkbox(r, key=key, value=st.session_state.checked_answers.get(key, False)):
                    user_checks.append(r)
                    st.session_state.checked_answers[key] = True
                else:
                    st.session_state.checked_answers[key] = False
            if user_checks == corrections:
                st.session_state.score += 1
        if st.button("Afficher le score final"):
            st.subheader("Score final :")
            st.write(st.session_state.score)
            st.session_state.score = 0


