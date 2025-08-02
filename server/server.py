from flask import Flask, jsonify, request
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URI")

client = MongoClient(mongo_uri)


@app.route("/")
def home():
  return f"Connected: {mongo_uri}"


@app.route("/insert", methods=["GET"])
def insert_sample():
    test_doc = {"name": "Test", "Test": True}
    result = client["terrahacks"]["test"].insert_one(test_doc)
    return jsonify({"inserted_id": str(result.inserted_id)})
