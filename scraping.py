import os
import serpapi
from serpapi import GoogleSearch
from openai import OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
GENAI_API_KEY = os.getenv("GENAI_API_KEY")

if not SERPAPI_KEY:
    raise ValueError("❌ SERPAPI_KEY is missing in .env file")

if not GENAI_API_KEY:
    raise ValueError("❌ GENAI_API_KEY is missing in .env file")


def google_scraping(key_json):
    query = f"{key_json.get('brand', '')} {key_json.get('product', '')}"

    # Initialize SerpAPI search
    search = GoogleSearch({
        "q": query,
        "engine": "google",
        "api_key": SERPAPI_KEY
    })

    results = search.get_dict()

    search_results = []
    for item in results.get("organic_results", []):
        link = item.get("link")
        if link:
            search_results.append(link)

    print("SERP Results:", search_results)

    gpt_response = ask_gemini(search_results, query)
    print("Gemini Response:", gpt_response)

    return "After Searching the Websites For More Details: " + str(gpt_response)[7:-3]


def ask_gemini(search_results, key):
    genai.configure(api_key=GENAI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

    cleaned_results = [str(x) for x in search_results]

    prompt = (
        "Go through the given website contents and extract the INGREDIENTS details "
        f"for the product: {key}\n\n"
        "Website data:\n"
        + "\n".join(cleaned_results)
        + "\nGive output in a JSON with 'ingredients' as the key."
    )

    response = model.generate_content(prompt)
    return response.text
