import google.generativeai as genai
from flask import Blueprint, request, jsonify

# Configure Google Gemini API
genai.configure(api_key="AIzaSyCCU8xmiAqtjpqrxiZypJqB3Cn_TQ5UzUQ")

# Create a Flask Blueprint for the AI Homework Bot
ai_homework_bot = Blueprint("ai_homework_bot", __name__)

@ai_homework_bot.route("/api/ai/help", methods=["POST"])
def ai_homework_help():
    """
    Flask endpoint to handle AI homework help requests.
    """
    try:
        # Get the question from the request JSON body
        data = request.get_json()
        question = data.get("question", "")
        
        if not question:
            return jsonify({"error": "No question provided."}), 400

        # Use the Google GenerativeAI model
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(question)
        
        # Return the AI-generated response
        return jsonify({"response": response.text}), 200

    except Exception as e:
        # Return error message in case of failure
        return jsonify({"error": str(e)}), 500
