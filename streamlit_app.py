import streamlit as st
import os
import openai
from legal_questions import define_legal_questions
from summary import summarize
from tagging import tag

openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

st.set_page_config(layout="wide")
st.title(":scales: Samenvatting en tagging :scales:")


if "legal_questions" not in st.session_state:
    st.session_state.legal_questions = None
if "summary_short" not in st.session_state:
    st.session_state.summary_short = ""
if "summary_long" not in st.session_state:
    st.session_state.summary_long = ""
if "tags" not in st.session_state:
    st.session_state.tags = ""
if "judgment" not in st.session_state:
    st.session_state.judgment = None

st.session_state.judgment = st.text_area(label="Plak hieronder de tekst van een vonnis of arrest")
if st.button("Tekst opladen"):
    if st.session_state.judgment:
        st.session_state.legal_questions = define_legal_questions(st.session_state.judgment)
        st.write("Tekst opgeladen")
    else:
        st.write("Geen tekst opgeladen")

if st.button("Beknopte samenvatting (max. 150):female-judge:"):
    st.session_state.summary_short = summarize(st.session_state.legal_questions, 150, st.session_state.judgment)

if st.button("Uitvoerige samenvatting (max. 300):female-judge:"):
    st.session_state.summary_long = summarize(st.session_state.legal_questions, 300, st.session_state.judgment)

if st.button('Genereer tags :female-judge:'):
    st.session_state.tags = tag(st.session_state.legal_questions)

if st.session_state.summary_short:
    st.header("Beknopte samenvatting")
    st.write(st.session_state.summary_short)
if st.session_state.summary_long:
    st.header("Uitvoerige samenvatting")
    st.write(st.session_state.summary_long)
if st.session_state.tags:
    st.header("Tags")
    st.write(st.session_state.tags)
