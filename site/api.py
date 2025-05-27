from flask import Flask, request, jsonify
from flask_cors import CORS
from finn import fetch_finn_jobs 

# it uses flask
app = Flask(__name__)
CORS(app)

#just its home route
@app.route("/")
def home():
    return "Flask is working!"

@app.route("/api/jobs", methods=["POST"])
def api_jobs():
    data = request.get_json()
    query = data.get("query")
    locations = data.get("locations")

    #standard error msg
    if not query or not locations:
        return jsonify({"error": "Missing query or locations"}), 400

    #get the function
    result = fetch_finn_jobs(query, locations)

    #make sure it can be read by js
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
