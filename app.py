from flask import Flask, render_template, request
import os
import cv2
import numpy as np
import easyocr
import google.generativeai as genai
from PIL import Image
import json
from scraping import google_scraping
reader = easyocr.Reader(['en'], gpu=False)
genai.configure(api_key="AIzaSyDL3nf20b25uobUYVnusB1Kt9OnfRKMwwI")
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index_new_newest.html')

@app.route('/process', methods = ['POST'])
def process_image():
    if 'image' not in request.files:
        return 'No image uploaded.', 400
    file = request.files['image']
    if file.filename == '':
        return 'No selected file.', 400
    if file:
        print("Received file:",file.filename)
        try:
            file_bytes = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("grey.png", grey)
            result = reader.readtext(grey)
            text = " ".join([res[1] for res in result])
            output_text = text
            gemini_understanding = model.generate_content("Understand the given text and take away any claims if any for the product or any benefits and store in a json as key(claims) no other content and the text is :"+ text)
            understanding = json.loads(gemini_understanding.text[7:-3])
            img = Image.open("grey.png")
            gemini_response = model.generate_content(
                ["""with the image can you extract primary keywords like brand and product
                "present get that and return {brand:,product:,website:}
                IF Ingredients are present like proper ingredients for the given image then add another key Ingredients = """, img]
            )
            gemini_out = gemini_response.text[7:-3]
            key_json = json.loads(gemini_out)
            key_json["claims"] = understanding["claims"]
            search_out = ''
            if "Ingredients" not in list(key_json.keys()):
                search_out = google_scraping(key_json)
            
            
            gemini_conclusion = model.generate_content("""You are a safety analyst. Here is Details you have:
                                                            claims :{}
                                                            Product : {}
                                                            Ingredients : {}
                                                            
                                                            Go through the ingredient and find any suspecious subtance
                                                            
                                                            And conclude if the claims in the text is true with the following ingredients.
                                                            
                                                            Extract any warnings (age restrictions, side effects, hazard notes).

                                                            Respond in strict JSON with fields and make the values short: product_name, short_summary, claims_finding, warnings or good content with a key like impact positive or negative(❌⚠️✅only for this field). and a overall Trust score number""".format(key_json["claims"],key_json["product"],search_out))
            
            gemini_conclusion_out = gemini_conclusion.text[7:-3]
            return render_template('index_new_newest.html', extracted_text=output_text,gemini_text=json.dumps(key_json),search_results=search_out,gemini_conclusion=gemini_conclusion_out) 
        
        except Exception as e:
            return f"An error occured: {e}", 500
        

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)