import serpapi
from openai import OpenAI
import google.generativeai as genai

def google_scraping(key_json):
    query = f"{key_json.get('brand', '')} {key_json.get('product', '')}"
    results = serpapi.search({
        "engine": "google",
        "q": query,
        "api_key": "87da85c27c533ff1a6c80cead0be691cc0ae011b1567aec280cac6d3c94346cb"
    })

    search_results = []
    for item in results.get("organic_results", []):
        link = item.get("link")
        if link:
            search_results.append(link)
    print(search_results)
    gpt_response = ask_gemini(search_results,query)
    print(gpt_response)
    return "After Searching the Websites For More Details"+str(gpt_response)[7:-3]

def ask_gemini(search_results, key):
    genai.configure(api_key="AIzaSyDL3nf20b25uobUYVnusB1Kt9OnfRKMwwI")
    model = genai.GenerativeModel("gemini-2.5-flash")
    cleaned_results = [str(x) for x in search_results]
    prompt = (
        "Go through the given website contents and extract the INGREDIENTS details "
        f"for the product: {key}\n\n"
        "Website data:\n"
        + "\n".join(cleaned_results)+ "give output in a json with ingredients as a key"
    )
    response = model.generate_content(prompt)
    return response.text