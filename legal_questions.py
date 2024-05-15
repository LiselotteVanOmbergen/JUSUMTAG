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


    # Get the generated output and replace '\\n' with '\n' for formatting
    output = completion.choices[0].message.content.replace('\\n', '\n')

    # Return the generated output
    return output
