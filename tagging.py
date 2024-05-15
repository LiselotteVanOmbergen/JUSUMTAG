import openai

# Example 
voorbeeld = "damage assessment - disability - temporary incapacity - commercial, economic, and financial law - insurance - public insurance law - defective product - damage according to article 1384 first paragraph bw - temporary disability - staff member - public sector"

def tag(legal_questions):
    # Client initialization
    client = openai.Client()
    # Create completion request
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

    # Get the generated output and replace '\\n' with '\n' for formatting
    output = completion.choices[0].message.content.replace('\\n', '\n')

    # Return the generated output
    return output
