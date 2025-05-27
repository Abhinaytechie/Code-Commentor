from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)


GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable not set.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

def generate_comments_gemini(code, language="python"):
    """Generates comments using the Gemini API."""
    
    prompt = f"Add simple comments to this {language} code:\n\n{code}\n\nCommented Code:"

    try:
        response = model.generate_content([{"text": prompt}])  # ✅ Corrected API call
        return response.text.strip() if response and response.text else "No response from API."
    
    except Exception as e:
        return f"Gemini API Error: {e}"



@app.route('/' ,methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/api/comment', methods=['GET','POST'])
def api_comment():
    data = request.get_json()
    code = data.get("code", "").strip()
    language = data.get("language", "python")

    if not code:
        return jsonify({"error": "No code provided"}), 400

    commented_code = generate_comments_gemini(code, language)
    return jsonify({"commented_code": commented_code})

if __name__ == '__main__':
    app.run(debug=True)
