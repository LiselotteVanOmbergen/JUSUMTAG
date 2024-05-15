import streamlit as st
import os
import openai
from legal_questions import define_legal_questions
from summary import summarize
from tagging import tag

openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

col1, col2 = st.columns(2)

file = st.text_input(label="")

legal_questions = None
summary_short = ""
summary_long = ""
tags = ""

if file:
    legal_questions = define_legal_questions(file)

with col1:
    st.header("Laad vonnis of arrest op")
    if file:
        st.write("File loaded:", file)
    else:
        st.write("No file loaded.")

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