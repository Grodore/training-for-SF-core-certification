import streamlit as st
import pandas as pd
import random

def select_random_elements_from_list(number_of_selection, liste):
    if number_of_selection > len(liste):
        return "Error: More elements requested than are available in the list."
    return random.sample(liste, number_of_selection)

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



cnx = st.connection("snowflake")
session = cnx.session()
#my_dataframe = session.table("SF_CORE_CERTIFICATION_TRAINING.TRAINING_DATA.QUESTIONS")
# Using Streamlit to display the data

df = fetch_data(session,nombre_de_question)
#afficher la première question
st.write(df['ENONCE'][0])
list = []
list = (df['REPONSES'][0])
st.write(list[0])



"""for index, row in df.iterrows():
    st.write(row['ENONCE'])
    for i in range(len(row['REPONSES'])):
        st.checkbox(row['REPONSES'][i])








if st.button("Mode examen, score et correction à la fin"):
    mode = 1
    st.write("Mode examen selectionné !")

if st.button("Mode entrainement, correction à chaque question"):
    mode = 2
    st.write("Mode entrainement selectionné !")"""




