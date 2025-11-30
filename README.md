Project : Agent Unveil

A Smart Detection Agent for Brand Misrepresentation
🔍 Overview
Consumers often rely on product images, descriptions, and marketing claims to make buying decisions.
However, brands sometimes exaggerate or misrepresent their products across e-commerce platforms, ads, and packaging.
This leads to poor purchasing decisions, financial loss, or safety concerns.

Manual monitoring is slow and impossible to scale.
This project uses agentic AI to automatically analyze and validate product information.

❗ Problem Statement

Consumers are often misled by brands that do not accurately depict their products in advertisements, packaging, or online descriptions.
Misrepresentation can cause:

Wrong purchasing decisions

Financial loss

Safety risks

Lack of trust in brands

Consumer authorities struggle to manually check thousands of listings across different websites.

💡 Solution

This project uses AI agents to autonomously analyze and verify product information from multiple channels.

The AI system can:

Collect data from e-commerce sites, social media ads, and brand pages.

Compare visuals and descriptions with real product information.

Detect inconsistencies such as fake claims, missing ingredients, misleading images.

Generate reports that highlight potential misrepresentation.

This creates a scalable, faster, and more accurate monitoring system that reduces human workload and protects consumers.

✨ Key Features

OCR extraction from product images

Identify product brand, product name, and claims

Fetch missing information using Google search (SerpAPI)

Extract ingredients using Gemini

Safety analysis using AI

Camera capture + multi-image upload support

Back-end built with Flask

Clean JSON-based AI responses

API keys securely stored using .env

📌 Table of Contents

About

Features

Tech Stack

Project Structure

Installation

Environment Variables

Running the App

API Endpoints

Screenshots

Contributing

License

📖 About

Write a short explanation of the project, why you built it, and what problem it solves.

✨ Features

Feature 1

Feature 2

Feature 3

🧰 Tech Stack

Frontend: React, Tailwind, etc
Backend: Flask, Node.js, FastAPI, etc
Database: PostgreSQL, MongoDB, etc
Other: Docker, Redis, etc


📂 Project Structure
Agent-Unveil/
│── app.py               # Main Flask backend
│── scraping.py          # Google scraping + Gemini ingredient extraction
│── templates/
│     └── index.html     # Frontend UI
│── requirements.txt     # Python dependencies
│── .env                 # Environment variables (hidden)
│── .gitignore           # Prevents .env and caches from being pushed
│── README.md            # Project documentation
│── grey.png             # Temporary OCR file
│── __pycache__/         # Python cache (ignored)


🛠 Installation

Clone the repo and install dependencies.

git clone https://github.com/yourname/yourrepo.git
cd yourrepo
pip install -r requirements.txt     # For Python
# or
npm install                         # For Node.js

🔑 Environment Variables

Create a .env file and add the required keys:

API_KEY=your_key
DATABASE_URL=your_connection_string
SECRET_KEY=your_secret

▶️ Running the App
Flask
flask run

Node
npm run dev

Docker
docker compose up --build

📡 API Endpoints (example)
Method	Endpoint	Description
GET	/api/products	Fetch all products
POST	/api/upload	Upload image or data
GET	/api/status	Health check
🖼 Screenshots

Add your screenshots here.

![Screenshot](images/screen1.png)

🤝 Contributing

Contributions are welcome!

Fork the repo

Create a new branch

Commit your changes

Create a pull request

📄 License

MIT License
You’re free to modify and use this project.

Agent Unveil Previews: 
<img width="1920" height="1152" alt="Screenshot 2025-11-29 110757" src="https://github.com/user-attachments/assets/4550bfe8-8fba-4b14-9222-592d22fffd22" />

<img width="1920" height="1152" alt="Screenshot 2025-11-29 111326" src="https://github.com/user-attachments/assets/01abda81-ceed-44c0-85f6-74cd1816156d" />

<img width="1920" height="1152" alt="Screenshot 2025-11-29 111445" src="https://github.com/user-attachments/assets/e83701a6-ae8f-428a-b6e3-95b649412cf6" />

<img width="1896" height="873" alt="1896_873_1 25" src="https://github.com/user-attachments/assets/97cf76d7-e4e2-49f9-bf68-cb33776d8d98" />

![Phone view of camera](https://github.com/user-attachments/assets/a4a501f7-da0e-4bd0-9557-0181f83e4e48)

<img width="1590" height="824" alt="1590_824_1 25" src="https://github.com/user-attachments/assets/b211764a-6b36-49cc-b45e-2bc7fac4ebf8" />

<img width="1872" height="770" alt="1872_770_1 25" src="https://github.com/user-attachments/assets/33ec2a77-248a-4d08-9269-ad71c5479803" />

<img width="1917" height="736" alt="1917_736_1 25" src="https://github.com/user-attachments/assets/a7787d59-c6da-4eb8-a824-3c1bd310f201" />










