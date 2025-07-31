from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Optional, Literal
import json

class Patient(BaseModel):

    id : Annotated[str, Field(..., description='ID of Patient', examples=['P001'])]
    name : Annotated[str, Field(..., max_length=30)]
    age : Annotated[int, Field(..., gt=0, lt=120)]
    height : Annotated[Optional[float], Field(default=None, description='Height of Patient in metres')]
    weight : Annotated[Optional[float], Field(default=None, description='Weight of Patient in kgs')]
    gender : Annotated[Literal['male', 'female', 'other'], Field(..., description='Gender of Patient')]
    cause : Annotated[str, Field(..., description='Cause of visiting')]

    @computed_field
    def bmi(self) -> float:

        if self.height and self.weight:
            bmi = round(self.weight/(self.height**2), 2)
            return bmi
        return None
    
    @computed_field
    def verdict(self) -> str:
        if self.bmi:
            if self.bmi < 18.5:
                return 'Underweight'
            if self.bmi <= 25:
                return 'Normal'
            if self.bmi < 30:
                return 'Overweight'
            else:
                return 'Obesity'
        return None
    
class PatientUpdate(BaseModel):

    name : Annotated[Optional[str], Field(default=None, max_length=30)]
    age : Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
    height : Annotated[Optional[float], Field(default=None, description='Height of Patient in metres')]
    weight : Annotated[Optional[float], Field(default=None, description='Weight of Patient in kgs')]
    cause : Annotated[Optional[str], Field(default=None, description='Cause of visiting')]
        
def saved(data):
    with open('patients.json', 'w') as f:
        json.dump(data, f)

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Welcome to HealthAI!"}

@app.get("/about")
def about():
    return {"message":"We serve patients with AI-powered health insights"}

def database():
    with open('patients.json', 'r') as f:
        db = json.load(f)
        return db

patients = database()
# patients = json.load(open("patients.json"))

@app.get("/view")
def view():
    return patients

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="Patient's ID", examples='P001')):
    if patient_id in patients:
        return patients[patient_id]
    raise HTTPException(status_code=404, detail="Patient Record Not Found!")

@app.get("/patients/sort")
def sort_patients(sort_by : str = Query(..., description="Sort patients by height, weight or age"), order : str = Query('asc',description="Sort by asc or desc order")):

    sort = ["height", "weight", "age"]

    if sort_by not in sort:
        raise HTTPException(status_code=400, detail=f"Only sort by {sort}")
    
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Say asc or desc to get ordered list of patients")
    
    order_condition = True if order == 'desc' else False
    
    sorted_patients = sorted(patients.values(), key=lambda x: x.get(sort_by, 0), reverse=order_condition)

    return sorted_patients

@app.post("/create")
def create_patient(patient: Patient):
    
    # loading our json file
    patients = database()

    # Check if a patient of id already exists
    if patient.id in patients:
        raise HTTPException(status_code=400, detail='Patient already exists!')

    # if patient doesn't already exitst, we create a new patient record with patient's ID as key
    # and convert the patient pydantic object into a dictionary by saying .model_dump() and adding it as the value of that key
    patients[patient.id] = patient.model_dump(exclude=['id'])

    # Saving the new record back into a json file
    saved(patients)

    return JSONResponse(status_code=201, content={'message': 'Patient Created Successfully!'})

@app.put('/edit/{patient_id}')
def update_patient(patient_id : str, updated_patient: PatientUpdate):

    # loading all the patients record
    patients = database()

    # checking if it already exists
    if patient_id not in patients:
        raise HTTPException(status_code=400, detail='Patient ID does not exist!') 
    
    # fetching the patients data by the key that user want to edit/update
    existing_patient_data = patients[patient_id]

    # fetching the fields from PatientUpdate pydantic model (made above) that the user updated
    # we're only getting those values that are set/changed/provided cuz all fields are optional when updating. 
    # we're not getting those fields that are unset
    updated_patient_data = updated_patient.model_dump(exclude_unset=True)

    # updating the only fields that user updated in that specific patient's record 
    for key, value in updated_patient_data.items():
        existing_patient_data[key] = value

    # Now because we also need bmi and verdict (those are computed fields) so we're creating a Patient Object
    # so that when values are passed in the Patient pydantic model, bmi and verdict is automatically calculated
    # now cuz existing_patient_data doesn't have 'id' field which is a required field in out Patient Pydantic model
    # we add the id field so we don't get an error
    existing_patient_data['id'] = patient_id
    patient_obj = Patient(**existing_patient_data)

    # now that computed fields are computed, we update the record in our patients database
    # and excluded the id field cuz that's what we're using as the key of each patient
    patients[patient_id] = patient_obj.model_dump(exclude='id')

    # saving it back into the patients db
    saved(patients)

    return JSONResponse(status_code=201, content={'message': 'Patient Record Updated Successfully!'})

@app.delete('/delete_patient/{patient_id}')
def delete_patient(patient_id: str):

    patients = database()

    if patient_id not in patients:
        raise HTTPException(status_code=404, detail='Patient Not Found!')

    del patients[patient_id]

    saved(patients)

    return JSONResponse(status_code=201, content={'message':'Patient Record Deleted!'})