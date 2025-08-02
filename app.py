from flask import Flask, jsonify, request, render_template, redirect
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import google.generativeai as genai

load_dotenv()

app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URI")
api_key = os.getenv("GEMINI_API_KEY")


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
  
@app.route("/delete/<id>", methods=["POST"])
def delete_patients(id):
  patientsCollection.delete_one({"_id": ObjectId(id)})
  return redirect("/patients")

@app.route("/patients", methods=["GET"])
def view_patients():
  patients = list(patientsCollection.find({}))
  return render_template("patients.html", patients=patients)

@app.route("/gemini", methods=["POST"])
def gemini():
  # Fetch all patients from MongoDB
  patients = list(patientsCollection.find({}, {"_id": 0}))
  # Prepare the prompt or data for Gemini
  
  # -------------To be edited by Prithvi--------------
  prompt = f"Here is the patient data: {patients}. What insights can you provide?"

  # Authenticate with Gemini
  genai.configure(api_key)
  model = genai.GenerativeModel("gemini-pro")
  response = model.generate_content(prompt)
  return jsonify({"gemini_response": response.text})