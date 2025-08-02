from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)
db = client["terrahacks"]
patientsCollection = db["patients"]


@app.route("/")
def index():
  return render_template("index.html")


@app.route("/add", methods=["POST"])
def add_patients():
    data = request.json
    patientsCollection.insert_one(data)
    return jsonify({"status": "ok"})
