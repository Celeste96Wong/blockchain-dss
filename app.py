"""
BlockchainReady — Flask Backend
Fuzzy MCDM Decision Support System for Blockchain Adoption
"""
from dotenv import load_dotenv
import os
load_dotenv()

from flask import Flask, render_template, request, jsonify
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core.fuzzy_engine import run_fuzzy_topsis, get_criteria_for_frontend
from core.ai_advisor import generate_recommendation

app = Flask(__name__)


@app.route("/")
def index():
    criteria = get_criteria_for_frontend()
    return render_template("index.html", criteria=criteria)


@app.route("/assess", methods=["POST"])
def assess():
    data = request.get_json()

    # Extract user inputs
    ratings = data.get("ratings", {})          # {criterion_id: 1-5}
    business_context = data.get("context", {}) # {industry, size, goal, api_key}

    # Convert string keys to int values
    int_ratings = {k: int(v) for k, v in ratings.items()}

    # Run Fuzzy TOPSIS
    topsis_result = run_fuzzy_topsis(int_ratings)

    # Generate AI recommendation
    ai_result = generate_recommendation(topsis_result, business_context)

    return jsonify({
        "topsis": topsis_result,
        "ai": ai_result,
    })


@app.route("/criteria")
def criteria():
    return jsonify(get_criteria_for_frontend())


if __name__ == "__main__":
    app.run(debug=True, port=5000)
