from flask import Flask, render_template, request
import os
import cv2
import numpy as np
import easyocr
import google.generativeai as genai
from PIL import Image
import json
import base64
from io import BytesIO
from scraping import google_scraping

reader = easyocr.Reader(['en'], gpu=False)
GENAI_API_KEY = os.getenv("GENAI_API_KEY")
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

app = Flask(__name__)


@app.route("/")
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_image():
    try:
        # ------------------------------------------------
        # 1. GET FILE UPLOAD OR CAMERA INPUT
        # ------------------------------------------------
        file = request.files.get("image")          # file input
        camera_image = request.form.get("cameraImage")   # base64 from camera

        img = None

        # CASE 1: File uploaded normally
        if file and file.filename != "":
            print("Received file:", file.filename)
            file_bytes = np.frombuffer(file.read(), np.uint8)
            img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        # CASE 2: Camera base64 image
        elif camera_image and camera_image.startswith("data:image"):
            print("Received camera image")
            header, encoded = camera_image.split(",", 1)
            img_data = base64.b64decode(encoded)
            pil_img = Image.open(BytesIO(img_data)).convert("RGB")
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

        else:
            return "No image uploaded from file or camera", 400

        # ------------------------------------------------
        # 2. OCR PROCESSING
        # ------------------------------------------------
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("grey.png", grey)

        result = reader.readtext(grey)
        text = " ".join([res[1] for res in result])
        output_text = text

        # ------------------------------------------------
        # 3. GEMINI: Extract claims
        # ------------------------------------------------
        gemini_understanding = model.generate_content(
            "Understand the given text and take away any claims if any for the product or any benefits "
            "and store in a json as key(claims) no other content and the text is :" + text
        )

        understanding = json.loads(gemini_understanding.text[7:-3])

        # ------------------------------------------------
        # 4. GEMINI: Extract brand/product/ingredients
        # ------------------------------------------------
        pil_img = Image.open("grey.png")
        gemini_response = model.generate_content(
            [
                """with the image can you extract primary keywords like brand and product
                present get that and return {brand:,product:,website:}
                IF Ingredients are present like proper ingredients for the given image then add another key Ingredients = """,
                pil_img
            ]
        )

        gemini_out = gemini_response.text[7:-3]
        key_json = json.loads(gemini_out)
        key_json["claims"] = understanding["claims"]

        # ------------------------------------------------
        # 5. Search scraping only if ingredients missing
        # ------------------------------------------------
        search_out = ""
        if "Ingredients" not in key_json:
            search_out = google_scraping(key_json)

        # ------------------------------------------------
        # 6. GEMINI final safety analysis
        # ------------------------------------------------
        gemini_conclusion = model.generate_content(
            """You are a safety analyst. Here is Details you have:
            claims :{}
            Product : {}
            Ingredients : {}
            
            Go through the ingredient and find any suspecious subtance
            
            And conclude if the claims in the text is true with the following ingredients.
            
            Extract any warnings (age restrictions, side effects, hazard notes).

            Respond in strict JSON with fields and make the values short: 
            product_name, short_summary, claims_finding, warnings 
            or good content with a key like impact positive or negative(❌⚠️✅only for this field), 
            overall Trust score number""".format(
                key_json["claims"], key_json["product"], search_out
            )
        )

        gemini_conclusion_out = gemini_conclusion.text[7:-3]

        # ------------------------------------------------
        # 7. Render results
        # ------------------------------------------------
        return render_template(
            'index.html',
            extracted_text=output_text,
            gemini_text=json.dumps(key_json),
            search_results=search_out,
            gemini_conclusion=gemini_conclusion_out
        )

    except Exception as e:
        return f"An error occurred: {e}", 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
