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
patients = list(patientsCollection.find({}))



@app.route("/")
def index():
  print(patients)
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
  return render_template("patients.html", patients=patients)

@app.route("/edit/<id>", methods=["GET"])
def edit_patients(id):
  patient = patientsCollection.find_one({"_id": ObjectId(id)})
  return render_template("edit.html", patient=patient)

@app.route("/update", methods=["POST"])
def update_patient():
    id = request.form["id"]
    updated_data = {
        "name": request.form["name"],
        "age": int(request.form["age"]),
        "height": request.form["height"],
        "weight": request.form["weight"],
        "incidentTime": request.form["incidentTime"],
        "admittanceTime": request.form["admittanceTime"],
        "concern": request.form["concern"]
    }
    patientsCollection.update_one(
        {"_id": ObjectId(id)},
        {"$set": updated_data}
    )
    return redirect("/patients")


@app.route("/gemini", methods=["POST"])
def gemini():  
  # -------------To be edited by Prithvi--------------
  prompt = f"Here is the patient data: {patients}. What insights can you provide?"

  # Authenticate with Gemini
  genai.configure(api_key)
  model = genai.GenerativeModel("gemini-pro")
  response = model.generate_content(prompt)
  return jsonify({"gemini_response": response.text})