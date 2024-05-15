import streamlit as st
import os
import openai
from legal_questions import define_legal_questions
from summary import summarize
from tagging import tag



openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

col1, col2 = st.columns(2)

with col1:
    st.header("Laad vonnis of arrest op")
    file = st.file_uploader()
    if file:
        legal_questions = define_legal_questions(file)

with col2:
    if file:
        if st.button("Beknopte samenvatting (max. 150)"):
            st.write(summarize(legal_questions, 150))

        if st.button("Uitvoerige samenvatting (max. 300)"):
            st.write(summarize(legal_questions, 300))

        if st.button('Genereer tags'):
            st.write(tag(legal_questions))
    else:
        st.write("Laad een bestand op om samenvattingen en tags te genereren.")