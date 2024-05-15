
import openai

voorbeeld = "begroting schade - arbeidsongeschiktheid - tijdelijke invaliditeit - handels-, economisch en financieel recht - verzekeringen - publiek verzekeringsrecht - gebrekkige zaak - schade conform artikel 1384 eerste lid bw - tijdelijke arbeidsongeschiktheid - personeelslid - publieke sector"


def tag(legal_questions):
    client = openai.Client()
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
    {"role": "system", "content": "Je bent een jurist."},
    {"role": "user", "content": f"""Geef de op juridisch vlak belangrijkste sleutelwoorden, afgeleid uit de gegeven rechtsvragen, zonder specifieke namen of feiten te gebruiken. 
Zorg ervoor dat de sleutelwoorden helder en beknopt zijn, zodat een jurist snel kan inschatten waar het vonnis of arrest over handelt. 
Voer uit naar analogie van het gegeven voorbeeld.
Scheid de woorden door middel van een koppelteken "-". 
Voorbeeld: {voorbeeld}
Rechtsvragen: {legal_questions}"""
}
    ]
)

# Haal de gegenereerde uitvoer op en vervang '\\n' met '\n' voor opmaak
    output = completion.choices[0].message.content.replace('\\n', '\n')

# Druk de gegenereerde uitvoer af
    return output
