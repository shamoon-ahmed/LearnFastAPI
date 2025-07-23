# Learning FastAPI

## Installation
**fastapi** for creating APIs, **uvicorn** where our server would be live, **pydantic** for data validation
```bash
pip install fastapi uvicorn pydantic
```

## Intialize FastAPI
Import libraries, instatiate FastAPI, and create a simple route
```bash
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message":"Welcome to HealthAI!"}
```
get means we're just retrieving some information from the server like retrieving data from the home page

run it with:
```bash
uvicorn filename:app --reload
```
-------------------

<br>

*Suppose we made a Patients Record Website and we have some patients' records in our DB (json in our case).*
<br>

*Whatever the case is, we can only do 4 operations*
- create - POST
- retrieve - GET
- update - PUT
- delete - DELETE

*Now lets load the json file of our patients records and do operations with it by adding different routes*
```bash
from fastapi import FastAPI, Path
import json

patients = json.load(open("patients.json"))

@app.get("/view")
def view():
    return patients
```
Just viewing all the patients records

-------------------

<br>

*If we want to view a specific patient's record*
```bash
@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="Patient's ID", example='P001')):
    if patient_id in patients:
        return patients[patient_id]
    return {"error":"No patient record found!"}
```
This works fine. One thing to keep in mind that there are status codes as well that tell what happened with our request.
<br>
Some common status codes are:
- 2xx - Success
- 3xx - The server directed us to some other page
- 4xx - No resource found
- 5xx - Server issue

But notice one thing, when we want the record of a patient who's not in the DB, the status code still says 200 which means success
<br>
This is wrong! So we need to handle this

```bash
from fastapi import FastAPI, Path, HTTPException
import json

@app.get("/patient/{patient_id}")
def view_patient(patient_id: str = Path(..., description="Patient's ID", example='P001')):
    if patient_id in patients:
        return patients[patient_id]
    raise HTTPException(status_code=404, detail="Patient Record Not Found!")
```
Now if we want patient P006 record (which is not available), the server will raise this exception and say 404 as the resource is not found

## Query Parameters 

*Now what if we want to sort patients by some characterstic and in ascending or descending order.*
<br>

*Means we need to filter out the data based on some conditions. Thats where we use **Query Paramters***

```bash
from fastapi import FastAPI, Path, HTTPException, Query

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
```
- First, we defined our route /patients/sort
- We defined the Query Paramter that our route will take - sort_by which is required (..., indicates required) and order which is optional
- We did error handling in case we get a bad request - Sending 400 status code
- Then sorted our patients based on the characterstics and order (if passed)
- *Our url will look something like this  ->* /patients/sort?sort_by=height&order=asc