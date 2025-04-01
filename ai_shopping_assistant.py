from flask import Flask, request, jsonify
import openai
from pyngrok import ngrok
import os

# Initialize Flask app
app = Flask(__name__)

# Set your OpenAI API Key (Replace with your actual OpenAI API key)
os.environ["OPENAI_API_KEY"] = "your-api-key"
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/ask", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  
            messages=[{"role": "user", "content": user_input}]
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Start Ngrok to expose the local server to the internet
port = 5000
public_url = ngrok.connect(port).public_url
print(f"Your assistant is running at: {public_url}")

# Run the Flask app
if __name__ == "__main__":
    app.run(port=port)
