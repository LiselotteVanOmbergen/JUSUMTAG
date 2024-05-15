
import openai

def summarize(legal_questions, max_words):
    client = openai.Client()
    completion = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
    {"role": "system", "content": "Je bent een jurist"},
    {"role": "user", "content": f"""Vermeld de wetsartikels en juridisch principes uit {legal_questions}. 
Je output bedraagt maximum {max_words} woorden, en bevat geen vermelding van de specifieke partijen, feiten of details van de zaak. 
Presenteer de tekst als een doorlopende tekst zonder enige onderverdelingen of ondertitels."""}
    ]
  
)

# Haal de gegenereerde uitvoer op en vervang '\\n' met '\n' voor opmaak
    output = completion.choices[0].message.content.replace('\\n', '\n')

# Druk de gegenereerde uitvoer af
    return "output"