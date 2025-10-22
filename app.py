from flask import Flask, request, jsonify
from similarity_search.similarity import get_similar

app = Flask(__name__)

@app.route("/")
def home():
    return "Flask Summarizer Running!"


@app.route("/ask",methods=["POST"])
def get_similars():
    response=""
    print("sending req")
    if(request.method=="POST"):
        data = request.get_json()
        text = data.get("query")
        print('here')
        response=get_similar(text)
        doc,score=response[0]
        pure_doc=doc.page_content
    print('hi')
    return jsonify({"response":{"doc":pure_doc,"score":score}})
    


if __name__ == "__main__":
    # port = int(os.environ.get("PORT", 8080))  # Use Railway's PORT or default to 8080
    # host = "0.0.0.0"  # Bind to all interfaces for Railway
    #app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    app.run(debug=True)
