
import requests
from flask import Flask, jsonify
import os
os.environ["FLASK_SKIP_DOTENV"] = "1"




app = Flask(__name__)

# Replace with your actual API key
RECIPEDB_BASE = "http://cosylab.iiitd.edu/recipe2-api"
FLAVORDB_BASE = "http://cosylab.iiitd.edu.in:6969/flavordb"

HEADERS = {
    "Authorization": "Bearer YOUR_API_KEY_HERE",
    "Content-Type": "application/json"
}

@app.route("/test-recipedb")
def test_recipedb():
    url = f"{RECIPEDB_BASE}/recipesinfo?page=0&size=5"
    response = requests.get(url, headers=HEADERS)
    return jsonify(response.json())

@app.route("/test-flavordb")
def test_flavordb():
    url = f"{FLAVORDB_BASE}/molecules_data/by-flavorProfile?flavorProfile=sweet&page=0&size=5"
    response = requests.get(url, headers=HEADERS)
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(debug=True)
