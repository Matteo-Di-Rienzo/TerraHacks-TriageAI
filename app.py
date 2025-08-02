from flask import Flask, jsonify, request, render_template, redirect
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os
import json
from vellum.client import Vellum
import vellum.types as types


load_dotenv()

app = Flask(__name__)
mongo_uri = os.getenv("MONGO_URI")
vellum_api_key = os.getenv("VELLUM_API_KEY")


client = MongoClient(mongo_uri)
db = client["terrahacks"]
patientsCollection = db["patients"]
patients = list(patientsCollection.find({}, {"_id": 0}))  # Exclude _id field

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



# pip install vellum-ai
client = Vellum(
  api_key=os.getenv["VELLUM_API_KEY"]
)
# patients_data = list(patientsCollection.find({}, {"_id": 0}))  # Get all patients, exclude _id
value_patients=json.dumps(patients)  # Convert to JSON string

result = client.execute_prompt(
    prompt_deployment_name="terra-hacks-er-triage-system-variant-1",
    release_tag="LATEST",
    inputs=[
        types.StringInputRequest(
            name="patients_list",
            value=value_patients,
        ),
    ],
)

if result.state == "REJECTED":
    raise Exception(result.error.message)

print(result.outputs)
