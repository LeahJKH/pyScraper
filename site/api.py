from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from finn import get_jobs  

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

    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    result = loop.run_until_complete(get_jobs(query, locations))

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database.connect import check_status

status = check_status()

if status == 1:
    print("We're good to go!")
else:
    print("Something went wrong with the DB connection.")