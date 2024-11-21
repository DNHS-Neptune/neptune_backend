from flask import Blueprint, request, jsonify
import google.generativeai as genai

genai.configure(api_key="AIzaSyCCU8xmiAqtjpqrxiZypJqB3Cn_TQ5UzUQ")
ai_homework_bot = Blueprint('ai_homework_bot', __name__)

@ai_homework_bot.route('/api/ai/help', methods=['POST'])
def ai_homework_help():
    data = request.get_json()
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "No question provided."}), 400

    try:
        response = genai.generate_text(prompt=question)
        return jsonify({"response": response.text}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
