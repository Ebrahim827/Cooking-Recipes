import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq
from dotenv import load_dotenv

# Load your .env file
load_dotenv()

app = Flask(__name__)
CORS(app) 

# Initialize Groq for recipe generation
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-recipe', methods=['POST'])
def get_recipe():
    user_input = request.json.get('ingredients')
    try:
        # Groq creates the recipe structure
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a chef. Return a recipe in JSON format with 'title', 'ingredients' (list), and 'instructions' (list)."},
                {"role": "user", "content": f"Ingredients: {user_input}"}
            ],
            response_format={"type": "json_object"}
        )
        # Return the AI JSON directly to the frontend
        return completion.choices[0].message.content

    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": str(e)}), 500

# UPDATED: This now sends your Google credentials safely to the HTML
@app.route('/get-google-config')
def get_google_config():
    return jsonify({
        "key": os.getenv("GOOGLE_API_KEY"),
        "cx": os.getenv("GOOGLE_CX")
    })

if __name__ == '__main__':
    # Local port 8888 is fine, PythonAnywhere will ignore this and use its own config
    app.run(host='127.0.0.1', port=8888, debug=True)