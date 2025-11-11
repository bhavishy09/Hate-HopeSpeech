from google import genai

client = genai.Client()

SYSTEM_PROMPT= """
You are a Content Creator Assistant you are supposed to help motivate and assist the content creators (specifically youtubers).
"""

MODEL_NAME = "gemini-2.5-flash"

def chatbot(prompt :str) -> str :
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=SYSTEM_PROMPT+prompt,
    )
    return response.text
