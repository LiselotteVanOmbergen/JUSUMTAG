import streamlit as st
import os
import openai
from legal_questions import define_legal_questions
from summary import summarize
from tagging import tag

openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

st.set_page_config(layout="wide")

col1, col2 = st.columns(2)

legal_questions = None
summary_short = ""
summary_long = ""
tags = ""

with col1:
    if st.button("tekst opladen"):
        #st.text_input(label="")
        file = st.text_area(label = "tekst vonnis of arrest")
        if file:
            st.write("Tekst opgeladen")
            st.write(legal_questions = define_legal_questions(file))
        else:
            st.write("Geen tekst opgeladen")


with col2:
    if file:
        if st.button("Beknopte samenvatting (max. 150)"):
            summary_short = summarize(legal_questions, 150)

        if st.button("Uitvoerige samenvatting (max. 300)"):
            summary_long = summarize(legal_questions, 300)

        if st.button('Genereer tags'):
            tags = tag(legal_questions)

st.write(summary_short)
st.write(summary_long)
st.write(tags)