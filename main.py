from fastapi import FastAPI, Path
import json

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Welcome to HealthAI!"}

@app.get("/about")
def about():
    return {"message":"We serve patients with AI-powered health insights"}

patients = json.load(open("patients.json"))

@app.get("/view")
def view():
    return patients

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="Patient's ID", example='P001')):
    if patient_id in patients:
        return patients[patient_id]
    return {"error":"No patient record found!"}