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
        "summary_short": "De rechtbank beoordeelt de zaak in het kader van de consumentenkoopwetgeving. Verweerster wordt beschouwd als verkoper, aangezien de verkoop plaatsvond in het kader van haar commerciële activiteit, ongeacht haar hoofdactiviteit. Eiser wordt als consument beschouwd, aangezien de aankoop voor privédoeleinden was. De rechtbank oordeelt dat het voertuig gebrekkig was bij levering en niet voldeed aan de normale verwachtingen van een dergelijk voertuig. Verweerster wordt aansprakelijk geacht voor de gebreken op basis van de consumentenkoopwetgeving. De rechtbank ontbindt de koopovereenkomst en veroordeelt verweerster tot terugbetaling van de koopsom en tot betaling van een bijkomende schadevergoeding aan eiser. De schadevergoeding omvat onder andere kosten voor takelen, expertise en belastingen. Verweerster's argument van schadebeperkingsplicht wordt verworpen, omdat herstel op haar rust.",
        "summary_long": """De rechtbank heeft vastgesteld dat de verweerster aansprakelijk is jegens de eiser op basis van de wetgeving over de consumentenkoop. Volgens artikel 1649 quater §1 B.W. is de verkoper aansprakelijk voor gebreken aan de geleverde goederen. In dit geval is de verweerster als professionele verkoper verantwoordelijk, omdat de verkoop van de auto plaatsvond in het kader van haar commerciële activiteit, ongeacht het feit dat haar hoofdactiviteit de verkoop van veranda's, ramen en deuren is.

De rechtbank oordeelde dat de eiser als consument kan worden beschouwd, aangezien hij de auto voor privédoeleinden heeft gekocht, ongeacht eventuele betrokkenheid van zijn echtgenoot en zoon in de autohandel.

Het voertuig vertoonde een gebrek aan overeenstemming bij levering, zoals bepaald in artikel 1604 en 1649ter van het Burgerlijk Wetboek. Dit werd aangetoond door het technisch advies waarin werd vastgesteld dat de motor defect was door een gebrek aan smering, wat resulteerde in een stukgeslagen drijfstang. Dit gebrek was aanwezig bij de levering van het voertuig en manifesteerde zich binnen zes maanden na de levering, waardoor het vermoeden ontstond dat het gebrek al bestond bij de levering.

De rechtbank oordeelde dat de eiser recht had op ontbinding van de koopovereenkomst en een bijkomende schadevergoeding, omdat de verweerster naliet om het voertuig kosteloos te herstellen of te vervangen. De verweerster werd veroordeeld tot terugbetaling van de koopsom, afgifte van het voertuig aan de eiser op haar kosten, en betaling van de gevorderde schadevergoeding, inclusief takelkosten, expertisekosten en belastingen.

De beslissing van de rechtbank volgt dus de dwingende regels voor consumentenkoop en geeft de eiser de remedies waar hij recht op heeft onder de wet.

""",
        "tags": "wetsartikel-1649quater-BW, consumentenkoop, gebrek aan overeenstemming, ontbinding, bijkomende schadevergoeding, herstel, vervanging, koopsom, expertiserapport, terugbetaling"
    },
    "Voorbeeld 2": {
        "text": "Dit is de tekst van het tweede vonnis of arrest.",
        "summary_short": "De belangrijkste rechtsvraag in dit vonnis betreft de ontvankelijkheid van een vordering tegen een rechtspersoon die niet langer bestaat ten tijde van de dagvaarding. Artikel 17 van het Gerechtelijk Wetboek vereist dat een rechtsvordering wordt ingesteld tegen diegene die de hoedanigheid bezit om ze te beantwoorden. Een exploit van dagvaarding tegen een niet-bestaande rechtspersoon leidt in principe tot onontvankelijkheid van de vordering. Dit geldt zelfs a fortiori wanneer de dagvaarding gericht is tegen een rechtspersoon die niet langer bestaat. Het niet naleven van deze fundamentele regel van identificatie van de verweerder kan niet worden gecompenseerd door andere formele vereisten. Het Grondwettelijk Hof heeft bevestigd dat deze regel van onontvankelijkheid relevant is om een goede rechtsbedeling te verzekeren en de risico's van rechtsonzekerheid te vermijden (Grondwettelijk Hof, Arrest 125/2014). Dit vonnis bevestigt de toepassing van deze regel en verklaart de vordering tegen de niet-bestaande rechtspersoon onontvankelijk, en vernietigt bijgevolg de veroordeling die daaruit voortvloeide.",
        "summary_long": """Het hof van beroep te Brussel heeft in het betreffende arrest een grondig oordeel geveld over de ontvankelijkheid van de vordering en de identificatie van de rechtspersoon die in de dagvaarding wordt genoemd. Het hof bevestigt dat een correcte identificatie van de gedaagde partij cruciaal is voor een rechtsgeldige procedure. Wanneer een exploit van dagvaarding de vermeldingen bevat die vereist zijn maar gericht is aan een andere persoon dan degene die zou moeten worden gedagvaard, leidt dit tot de onontvankelijkheid van de vordering.
In dit specifieke geval betoogde MS AMLIN INSURANCE SE dat de dagvaarding aan NV AMLIN EUROPE werd betekend, een entiteit die op dat moment niet meer bestond. Het hof oordeelt dat dit niet louter een vormgebrek betreft, maar een daadwerkelijke vergissing in de identificatie van de gedaagde partij. Het feit dat de namen, rechtsvormen, nationaliteiten, KBO-nummers en maatschappelijke zetels van de entiteiten verschillen, onderstreept deze vergissing. Bijgevolg verklaart het hof de vordering tegen NV AMLIN EUROPE onontvankelijk en vernietigt de veroordeling in eerste aanleg.
De incidentele vordering van A.A. tegen MS AMLIN INSURANCE SE in hoger beroep wordt echter afgewezen omdat dit een nieuwe vordering is tegen een partij die geen partij was in eerste aanleg. Dit arrest benadrukt dus het belang van een correcte identificatie van partijen in gerechtelijke procedures en bevestigt de noodzaak van het vermijden van vergissingen in dit opzicht om een eerlijke en geldige rechtsgang te waarborgen.
""",
        "tags": "beroepsaansprakelijkheid-verzekeraar-schadevergoeding-hoger-beroep-vormgebreken-ontvankelijkheid-fusie-identificatie-vennootschap-Gerechtelijk-Wetboek"
    },
    "Voorbeeld 3": {
        "text": "Dit is de tekst van het derde vonnis of arrest.",
        "summary_short": "De abstracte juridische conclusie uit het arrest van het hof van beroep te Brussel, met betrekking tot de toepassing van dwangbevelen, is dat dwangbevelen enkel kunnen worden gebruikt voor de invordering van vaststaande schuldvorderingen, zoals bepaald door artikel 3 van de Domaniale wet van 22 december 1949. Dit betekent dat, indien de schuldvordering betwist wordt, zoals in het geval van voortdurende correspondentie tussen de partijen over de verschuldigde bedragen, het dwangbevel niet als vaststaand beschouwd kan worden, waardoor de tenuitvoerlegging ervan niet kan doorgaan totdat de rechtsgeldigheid en de vaststelling van de schuldvordering definitief is beslist. Dit principe benadrukt dat voor het gebruik van dwangbevelen als middel tot invordering, de schuld onbetwist en duidelijk vastgesteld moet zijn.",
        "summary_long": """Het Hof van Beroep te Brussel heeft in het uitgesproken arrest beoordeeld dat het dwangbevel dat door de Belgische Staat FOD Binnenlandse Zaken was uitgevaardigd tegen het Vlaamse Gewest niet nietig verklaard kan worden, ondanks de betwisting van de onderliggende schuldvordering. Het Hof concludeerde dat hoewel er betwisting bestond over de schuldvordering, dit niet automatisch leidt tot nietigverklaring van het dwangbevel, aangezien de wet geen nietigheidssanctie voorziet. Het Hof oordeelde dat de tenuitvoerlegging van het dwangbevel niet kon plaatsvinden totdat er een uitspraak was gedaan over het vaststaand karakter van de schuldvordering.
Verder stelde het Hof vast dat de verjaring van de vordering van de Belgische Staat FOD Binnenlandse Zaken niet was ingetreden op het moment van de uitvaardiging van het dwangbevel. Het Hof baseerde dit op de toepassing van artikel 2262bis §1, 1ste lid van het oud Burgerlijk Wetboek, dat een verjaringstermijn van tien jaar bepaalt. Bovendien wees het Hof erop dat de kosten voor het opruimen van dierlijk afval, uitgevoerd door de civiele bescherming, verhaald kunnen worden op de begunstigde van de prestaties, zijnde het Vlaamse Gewest, in wiens belang de interventie was uitgevoerd.
Concluderend heeft het Hof het hoger beroep van het Vlaamse Gewest ongegrond verklaard en heeft het de vordering van de Belgische Staat FOD Binnenlandse Zaken tot betaling van de kosten voor het opruimen van dierlijk afval door de civiele bescherming toegewezen, met inbegrip van intresten aan de wettelijke intrestvoet
.""",
        "tags": "Overheidsaansprakelijkheid - wettelijke-verplichting - kostenverhaal - verjaring - dwangbevel"
    },
    "Voorbeeld 4": {
        "text": "Dit is de tekst van het vierde vonnis of arrest.",
        "summary_short": """De belangrijkste abstracte juridische conclusie die kan worden getrokken uit dit vonnis is dat een rechtskeuze voor een bepaald huwelijksvermogensstelsel door echtgenoten geldig kan worden vastgesteld door een gedateerd en door beide echtgenoten ondertekend geschrift, conform artikel 52, eerste lid van het Wetboek van Internationaal Privaatrecht. Deze vormvoorwaarde heeft tot doel de wilsovereenstemming van de echtgenoten met zekerheid vast te stellen. Indien een dergelijk geschrift voorhanden is waarin de echtgenoten expliciet voor een bepaald nationaal huwelijksvermogensstelsel hebben gekozen, is er sprake van een geldige rechtskeuze die moet worden gerespecteerd, zelfs indien deze keuze dateert van vóór de inwerkingtreding van het huidige Wetboek IPR (artikel 127, §2 WIPR). Deze principes vloeien voort uit de artikelen 49, 50, 52 en 127, §2 van het Wetboek van Internationaal Privaatrecht, in samenhang met de algemene beginselen inzake de totstandkoming van overeenkomsten en de interpretatie van wilsuitingen.
""",
        "summary_long": """Het hof heeft het bestreden vonnis van 11 december 2019 van de familierechtbank bij de rechtbank van eerste aanleg te Brussel beoordeeld, waarin het advies van notaris Tom Verhaegen werd bevestigd. Het vonnis bepaalde dat het Italiaanse recht van toepassing is op de verrichtingen van vereffening en verdeling van het huwelijksvermogensstelsel van de partijen, met name het Italiaanse stelsel van scheiding van goederen. Het hof heeft vastgesteld dat de notaris, de eerste rechter en geïntimeerde van mening waren dat er een geldige rechtskeuze was gemaakt voor het Italiaanse recht en het Italiaanse stelsel van scheiding van goederen. De partijen waren gehuwd vóór de inwerkingtreding van het Wetboek op het internationaal privaatrecht (WIPR), maar artikel 127, §2 WIPR valideert een rechtskeuze die voldoet aan de voorwaarden van deze wet. Het hof heeft de geldigheid van de rechtskeuze onderzocht aan de hand van de bepalingen van het WIPR, met name artikel 49, 50 en 52. Uit de stukken blijkt dat partijen expliciet hebben gekozen voor het Italiaanse stelsel van scheiding van goederen, zoals vermeld in de huwelijksakte die door beide echtgenoten, de priester en getuigen is ondertekend. Het hof heeft geoordeeld dat deze rechtskeuze geldig is volgens het Italiaanse recht en de bepalingen van het WIPR. Daarom heeft het hof het hoger beroep van appellant afgewezen en het bestreden vonnis bevestigd.

""",
        "tags": "Echtscheiding, Huwelijksvermogensrecht, Scheiding van goederen, Rechtskeuze, Gerechtelijke vereffening-verdeling, Tijdige mededeling stukken, Procedurewet, WIPR, Belgisch recht, Italiaans recht."
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
