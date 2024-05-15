import streamlit as st
import os
import openai
from legal_questions import define_legal_questions
from summary import summarize
from tagging import tag

openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

st.set_page_config(layout="wide")
st.title(":scales: Samenvatting en tagging :scales:")

# Initialize session state variables
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

# Upload Text Section
st.header("Upload Tekst")
text_area_judgment = st.text_area(label="Plak hieronder de tekst van een vonnis of arrest")
col1, col2 = st.columns(2)
with col1:
    if st.button("Tekst opladen :spiral_note_pad:"):
        if text_area_judgment:
            st.session_state.judgment = text_area_judgment
            st.session_state.legal_questions = define_legal_questions(text_area_judgment)
            st.write("Tekst opgeladen")
        else:
            st.write("Geen tekst opgeladen")

# Add separator
st.write("---")

# Summarize Section
st.header("Samenvatting")
with col1:
    if st.button("Beknopte samenvatting (max. 150):female-judge:"):
        st.session_state.summary_short = summarize(st.session_state.legal_questions, 150, st.session_state.judgment)
with col2:
    if st.button("Uitvoerige samenvatting (max. 300):female-judge:"):
        st.session_state.summary_long = summarize(st.session_state.legal_questions, 300, st.session_state.judgment)

# Add separator
st.write("---")

# Tags Section
st.header("Tags")
with col1:
    if st.button('Genereer tags :female-judge:'):
        st.session_state.tags = tag(st.session_state.legal_questions)

# Add separator
st.write("---")

# Display summaries and tags if available
if st.session_state.summary_short:
    st.subheader("Beknopte samenvatting")
    st.write(st.session_state.summary_short)
    st.download_button("Download beknopte samenvatting", st.session_state.summary_short, file_name="beknopte_samenvatting.txt", mime="text/plain")
if st.session_state.summary_long:
    st.subheader("Uitvoerige samenvatting")
    st.write(st.session_state.summary_long)
    st.download_button("Download uitvoerige samenvatting", st.session_state.summary_long, file_name="uitvoerige_samenvatting.txt", mime="text/plain")
if st.session_state.tags:
    st.subheader("Tags")
    st.write(st.session_state.tags)
    st.download_button("Download tags", st.session_state.tags, file_name="tags.txt", mime="text/plain")

# Shareable link
st.subheader("Deelbare link")
shareable_link = st.text_input("Kopieer en deel deze link", value=st.script_request_queue.get_current().get_pathname(), readonly=True)
