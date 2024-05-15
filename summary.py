import openai

# Example
voorbeeld = """Het dagvaarden van de verkeerde persoon moet in beginsel leiden tot de onontvankelijkheid van de vordering op grond van artikel 17 Ger.W. Dit geldt des te meer voor het aanspreken van een niet meer bestaande persoon. Dergelijke onregelmatigheid valt buiten de werkingssfeer van de nietigheidsregeling van de artikelen 860 tot 867 Ger.W., en geeft dienvolgens geen aanleiding tot beoordeling van belangenschade. In voorliggend geval bevatte de dagvaarding weliswaar de vermeldingen als voorzien in de artikelen 43 en 702, 2° Ger.W., maar werd een andere naam, rechtsvorm, nationaliteit, KBO-nummer en maatschappelijke zetel vermeld. In dit geval is er dus geen sprake van een vormgebrek bij de aanduiding van de juiste rechtspersoon, maar wordt er daarentegen een andere rechtspersoon aangeduid. De vordering wordt onontvankelijk verklaard."""

def summarize(legal_questions, max_words, judgment):
    # Client initialization
    client = openai.Client()
    # Create completion request
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Je bent een jurist"},
            {"role": "user", "content": f"""Wat zijn de antwoorden op de rechtsvragen en subvragen, vermeld in {legal_questions}, in het gegeven vonnis of arrest? 
            Vermeld de wetsartikels en juridisch principes uit jouw antwoord. Je output bedraagt maximum 150 woorden, en bevat geen vermelding van de specifieke partijen, feiten of details van de zaak. Presenteer de tekst als een doorlopende tekst zonder enige onderverdelingen of ondertitels.{legal_questions}. 
            Je output bedraagt maximum {max_words} woorden, en bevat geen vermelding van de specifieke partijen, feiten of details van de zaak. 
            Presenteer de tekst als een doorlopende tekst zonder enige onderverdelingen of ondertitels.
            Voer uit naar analogie met gegeven voorbeeld.
            Vonnis of arrest: {judgment}
            Voorbeeld: {voorbeeld}"""}
        ]
    )

    # Get the generated output and replace '\\n' with '\n' for formatting
    output = completion.choices[0].message.content.replace('\\n', '\n')

    # Return the generated output
    return output
