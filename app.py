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
    
    #boucle pour supprimer les crochets
    for i in cadre:
        chaine = chaine.replace(i, "")
    liste = chaine.split(',')
    for i in range(len(liste)):
        liste[i] = liste[i].strip()
    return liste



# Assuming you have a session to Snowflake already established
def fetch_data(session,number_of_rows_to_fetch=10):
    lenmax = 50  # Maximum ID value
    random_ids = random.sample(range(1, lenmax + 1), number_of_rows_to_fetch)
    id_list = ', '.join(map(str, random_ids))

    query = f"""
    SELECT * FROM SF_CORE_CERTIFICATION_TRAINING.TRAINING_DATA.QUESTIONS
    WHERE ID IN ({id_list})
    """
    df = session.sql(query).to_pandas()
    return df


st.title('Application d\'entrainement pour la certification Snowflake Core')

nombre_de_question =st.selectbox("Nombre de questions", list(range(1,50)))
mode = 0
score = 0
indexkey = 0





cnx = st.connection("snowflake")
session = cnx.session()
#my_dataframe = session.table("SF_CORE_CERTIFICATION_TRAINING.TRAINING_DATA.QUESTIONS")
# Using Streamlit to display the data

if 'df' not in st.session_state:
    st.session_state.df = fetch_data(session,nombre_de_question)



if st.button("Mode examen, score et correction à la fin"):
    st.session_state.mode = 1
    st.write("Mode examen selectionné !")

if st.button("Mode entrainement, correction à chaque question"):
    st.session_state.mode = 2
    st.write("Mode entrainement selectionné !")



if st.session_state.mode == 1:
    st.session_state.setdefault('mode', 0)
    st.session_state.setdefault('score', 0)
    st.session_state.setdefault('indexkey', 0)

    for index, row in st.session_state.df.iterrows():
        st.subheader("Question " + str(index+1))
        st.write(row['ENONCE'])
        rep_list = []
        rep_list = extraction_des_reponses(st.session_state.df['REPONSES'][index])
        corrections = []
        corrections = extraction_des_reponses(st.session_state.df['CORRECTION'][index])
        checked = []
        for r in rep_list:
            st.session_state.indexkey+=1
            if st.checkbox(r, key=st.session_state.indexkey):
                checked.append(r)
        if checked == corrections:
            st.session_state.score +=1
            
    st.write("Score final : ", st.session_state.score)