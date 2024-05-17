import streamlit as st
import os
import openai
from legal_questions import define_legal_questions
from summary import summarize
from tagging import tag

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY"))

# Set layout configuration
st.set_page_config(layout="wide")
st.title(":scales: Samenvatten en taggen :scales:")

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

# Hardcoded examples
examples = {
    "Voorbeeld 1": "Onderwerp",
    "Voorbeeld 2": "Dit is de tekst van het tweede vonnis of arrest.",
    "Voorbeeld 3": "Dit is de tekst van het derde vonnis of arrest."
}

# Dropdown to select example
selected_example = st.selectbox("Kies een voorbeeld", list(examples.keys()))
# Text upload section
text_area_judgment = st.text_area(label="Plak hieronder de tekst van het vonnis of arrest")

# Button to upload text
if st.button("Tekst opladen :spiral_note_pad:"):
    if text_area_judgment:
        st.session_state.judgment = text_area_judgment
        st.session_state.legal_questions = define_legal_questions(text_area_judgment)
        st.write("Tekst opgeladen")
    else:
        st.write("Geen tekst opgeladen")

# Add horizontal line to separate sections
st.write("---")

# Create three columns for buttons
col1, col2, col3 = st.columns(3)

# Button to generate concise summary
with col1:
    if st.button("Beknopte samenvatting (max. 150 woorden):female-judge:"):
            st.session_state.summary_short = summarize(st.session_state.legal_questions, 150, st.session_state.judgment)
       
            
# Button to generate detailed summary
with col2:
    if st.button("Uitvoerige samenvatting (max. 300 woorden):female-judge:"):
        st.session_state.summary_long = summarize(st.session_state.legal_questions, 300, st.session_state.judgment)

# Button to generate tags
with col3:
    if st.button('Genereer tags :female-judge:'):
        st.session_state.tags = tag(st.session_state.legal_questions)

# Display generated summaries and tags
if st.session_state.summary_short:
    st.subheader("Beknopte samenvatting")
    st.write(st.session_state.summary_short)
    st.download_button("Download beknopte samenvatting", st.session_state.summary_short, file_name="concise_summary.txt", mime="text/plain")
if st.session_state.summary_long:
    st.subheader("Uitvoerige samenvatting")
    st.write(st.session_state.summary_long)
    st.download_button("Download uitvoerige samenvatting", st.session_state.summary_long, file_name="detailed_summary.txt", mime="text/plain")
if st.session_state.tags:
    st.subheader("Tags")
    st.write(st.session_state.tags)
    st.download_button("Download tags", st.session_state.tags, file_name="tags.txt", mime="text/plain")

