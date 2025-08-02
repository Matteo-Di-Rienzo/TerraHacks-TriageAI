from flask import Flask, jsonify, request
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
def home():
  return f"Connected: {mongo_uri}"


@app.route("/add", methods=["POST"])
def add_patients():
    data = request.json
    patientsCollection.insert_one(data)
    return jsonify({"status": "ok"})
