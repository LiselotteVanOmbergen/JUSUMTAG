import streamlit as st
import os
import openai
from legal_questions import define_legal_questions
from summary import summarize
from tagging import tag

openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

st.set_page_config(layout="wide")
st.header(":scales:")


if "legal_questions" not in st.session_state:
    st.session_state.legal_questions = None
if "summary_short" not in st.session_state:
    st.session_state.summary_short = ""
if "summary_long" not in st.session_state:
    st.session_state.summary_long = ""
if "tags" not in st.session_state:
    st.session_state.tags = ""

file = st.text_area(label="Plak hier de tekst van een vonnis of arrest")
if st.button("Tekst opladen"):
    if file:
        st.session_state.legal_questions = define_legal_questions(file)
        st.write("Tekst opgeladen")
    else:
        st.write("Geen tekst opgeladen")

if st.button("Beknopte samenvatting (max. 150):female-judge:"):
    st.session_state.summary_short = summarize(st.session_state.legal_questions, 150)

if st.button("Uitvoerige samenvatting (max. 300):female-judge:"):
    st.session_state.summary_long = summarize(st.session_state.legal_questions, 300)

if st.button('Genereer tags :female-judge:'):
    st.session_state.tags = tag(st.session_state.legal_questions)

st.write(st.session_state.summary_short)
st.write(st.session_state.summary_long)
st.write(st.session_state.tags)
