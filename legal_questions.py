import openai

def define_legal_questions(judgment):
    client = openai.Client()
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
    {"role": "system", "content": "Je bent een jurist"},
    {"role": "user", "content": f"""Geef de belangrijkste rechtsvragen, subvragen, wetsartikels en juridische principes in het gegeven vonnis of arrest
zonder vermelding van de specifieke partijen, feiten of details van de zaak. Vonnis of arrest: {judgment}"""}
    ]
   

)

# Haal de gegenereerde uitvoer op en vervang '\\n' met '\n' voor opmaak
    output = completion.choices[0].message.content.replace('\\n', '\n')

# Druk de gegenereerde uitvoer af
    return output
