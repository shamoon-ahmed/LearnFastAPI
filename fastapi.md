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

<br>

*Suppose we made a Patients Record Website and we have some patients' records in our DB (json in our case).*
<br>

*Whatever the case is, we can only do 4 operations*
- create - POST
- retrieve - GET
- update - PUT
- delete - DELETE

