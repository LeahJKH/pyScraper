from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from finn import fetch_finn_jobs_async  # use the async version directly

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Flask is working!"

@app.route("/api/jobs", methods=["POST"])
def api_jobs():
    data = request.get_json()
    query = data.get("query")
    locations = data.get("locations")

    if not query or not locations:
        return jsonify({"error": "Missing query or locations"}), 400

    # Await the async job fetcher
    result = asyncio.run(fetch_finn_jobs_async(query, locations))

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
