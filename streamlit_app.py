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
if "example" not in st.session_state:
    st.session_state.example = None

# Hardcoded examples with summaries and tags
examples = {
    "Voorbeeld 1": {
        "text": "Dit is de tekst van het eerste vonnis of arrest.",
        "summary_short": "Beknopte samenvatting van voorbeeld 1.",
        "summary_long": "Uitvoerige samenvatting van voorbeeld 1.",
        "tags": "Tag1, Tag2, Tag3"
    },
    "Voorbeeld 2": {
        "text": "Dit is de tekst van het tweede vonnis of arrest.",
        "summary_short": "Beknopte samenvatting van voorbeeld 2.",
        "summary_long": "Uitvoerige samenvatting van voorbeeld 2.",
        "tags": "Tag4, Tag5, Tag6"
    },
    "Voorbeeld 3": {
        "text": "Dit is de tekst van het derde vonnis of arrest.",
        "summary_short": "Beknopte samenvatting van voorbeeld 3.",
        "summary_long": "Uitvoerige samenvatting van voorbeeld 3.",
        "tags": "Tag7, Tag8, Tag9"
    },
    "Voorbeeld 4": {
        "text": "Dit is de tekst van het vierde vonnis of arrest.",
        "summary_short": "Beknopte samenvatting van voorbeeld 4.",
        "summary_long": "Uitvoerige samenvatting van voorbeeld 4.",
        "tags": "Tag10, Tag11, Tag12"
    }
}
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        st.text("1. Kies een uitgewerkt voorbeeld")
        example_cols = st.columns(4)
        example_buttons = list(examples.keys())

        for example in example_buttons:
            with example_cols[example_buttons.index(example)]:
                if st.button(example):
                    st.session_state.summary_short = ""
                    st.session_state.summary_long = ""
                    st.session_state.tags = ""
                    st.session_state.example = example

    # Text upload section
    with col2:
        st.text("2. Of plak hieronder de tekst van een vonnis of arrest en laad het op")
        text_area_judgment = st.text_area(label ="")

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
        if st.session_state.judgment:
            st.session_state.summary_short = summarize(st.session_state.legal_questions, 150, st.session_state.judgment)
        elif st.session_state.example:
            st.session_state.summary_short = examples[st.session_state.example]["summary_short"]

# Button to generate detailed summary
with col2:
    if st.button("Uitvoerige samenvatting (max. 300 woorden):female-judge:"):
        if st.session_state.judgment:
            st.session_state.summary_long = summarize(st.session_state.legal_questions, 300, st.session_state.judgment)
        elif st.session_state.example:
            st.session_state.summary_long = examples[st.session_state.example]["summary_long"]

# Button to generate tags
with col3:
    if st.button('Genereer tags :female-judge:'):
        if st.session_state.judgment:
            st.session_state.tags = tag(st.session_state.legal_questions)
        elif st.session_state.example:
            st.session_state.tags = examples[st.session_state.example]["tags"]

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
