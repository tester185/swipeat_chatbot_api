from flask import Flask, request, jsonify
import os
from ai_chatbot.ai_chatbot import get_response

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask Summarizer Running!"


@app.route("/ask",methods=["POST"])
def get_categories():
    response=""
    print("sending req")
    if(request.method=="POST"):
        data = request.get_json()
        text = data.get("query")
        print('here')
        response=get_response(text)
    print('hi')
    return jsonify({"response":response})
    


if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 8080))  # Use Railway's PORT or default to 8080
    # host = "0.0.0.0"  # Bind to all interfaces for Railway
    #app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    app.run(debug=True)
