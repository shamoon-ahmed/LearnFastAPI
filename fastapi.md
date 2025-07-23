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
Now if we want patient P006 record (which is not available), the server will raise this exception

-------------------

