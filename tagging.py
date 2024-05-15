
import openai

voorbeeld = """Begroting schade - Arbeidsongeschiktheid - Tijdelijke invaliditeit
HANDELS-, ECONOMISCH EN FINANCIEEL RECHT - VERZEKERINGEN - Publiek verzekeringsrecht -	
Gebrekkige zaak - schade conform artikel 1384 eerste lid BW - tijdelijke arbeidsongeschiktheid - personeelslid - publieke sector"""

def tag(legal_questions):
    client = openai.Client()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "Je bent een jurist."},
    {"role": "user", "content": f"""Geef op basis van {legal_questions} de op juridisch vlak belangrijkste sleutelwoorden van het vonnis of arrest, zonder specifieke namen of feiten te gebruiken. 
Zorg ervoor dat de sleutelwoorden helder en beknopt zijn, zodat een jurist snel kan inschatten waar het vonnis of arrest over handelt. 
Volg de exact de structuur van het gegeven voorbeeld.
Scheid de woorden door middel van een koppelteken "-". 
Voorbeeld: {voorbeeld.lower}"""}
    ]
)

# Haal de gegenereerde uitvoer op en vervang '\\n' met '\n' voor opmaak
    output = completion.choices[0].message.content.replace('\\n', '\n')

# Druk de gegenereerde uitvoer af
    return output
