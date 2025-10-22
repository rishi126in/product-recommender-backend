import os
import requests
from dotenv import load_dotenv
from api.utils import get_products

load_dotenv()
API_KEY = os.getenv("MISTRAL_API_KEY")

MISTRAL_URL = "https://api.openrouter.ai/v1/chat/completions"

def get_recommendations(user_query, top_k=5):
    products = get_products()
    # Build a prompt for Mistral
    prompt = f"""
You are a product recommendation assistant.
Recommend the top {top_k} products from the following list that best match the user query: "{user_query}".

Products:
"""
    for p in products:
        prompt += f"- {p['title']}: {p.get('category','')} ({p.get('dimension','')})\n"

    prompt += "\nReturn only a JSON list of product titles in order of relevance."

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1
    }
    response = requests.post(MISTRAL_URL, headers=headers, json=data, timeout=30)
    res_json = response.json()

    # Extract assistant message
    message = res_json['choices'][0]['message']['content']

    import json
    try:
        recommended_titles = json.loads(message)
    except:
        recommended_titles = []

    # Match titles to full product data
    recommended_products = [p for p in products if p['title'] in recommended_titles]
    return recommended_products
