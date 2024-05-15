import streamlit as st
import os
import openai
from summary import summarize
from tagging import tag
from legal_questions import define_legal_questions


openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

col1, col2 = st.columns(2)

with col1:

    st.header("Laad vonnis of arrest op")
    file = st.file_uploader()

with col2:
    
    if st.button("Beknopte samenvatting (max. 150)"):
        legal_questions = define_legal_questions(file)
        st.write(summarize(legal_questions, 150)),
        legal_questions = define_legal_questions(file)
    if st.button("Uitvoerige samenvatting (max. 300)"):
        legal_questions = define_legal_questions(file)
        st.write(summarize(legal_questions, 300)),
    if st.button('Genereer tags'):
        st.write(tag(legal_questions))
