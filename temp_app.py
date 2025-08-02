from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["terrahacks"]
patientsCollection = db["patients"]


# @app.route("/")
# def home():
#   return f"Connected: {mongo_uri}"

@app.route("/", methods=["GET", "POST"])
def index():
  submitted = False
  data = {}
  if request.method == "POST":
      data["name"] = request.form.get("name")
      data["color"] = request.form.get("color")
      submitted = True
      client["terrahacks"]["submissions"].insert_one(data)
  return render_template("index.html", submitted=submitted, data=data)

@app.route("/insert", methods=["GET"])
def insert_sample():
    test_doc = {"name": "Test", "Test": True}
    result = client["terrahacks"]["test"].insert_one(test_doc)
    return jsonify({"inserted_id": str(result.inserted_id)})

if __name__ == "__main__":
    app.run(debug=True)