from fastapi import FastAPI, Path

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, FastAPI!"}

'''
GET - RETRIEVE INFORMATION
POST - Create something 
PUT - Update 
DELETE - Delete something
'''

'''
To run: uvicorn main:app --reload
'''
###### End point ##########
@app.get("/about")
def about():
    return {
        "name": "Pratik",
        "role": "ML Engineer",
        "language": "Python"
    }

####### Path Parameneters ########
@app.get("/hello/{name}")
def greet(name: str):
    return {
        "message": f"Hello {name}"
    }

@app.get("/square/{number}")
def square(number: int):
    return {
        "number": number,
        "square": number ** 2
    }

##### query parameters ######
@app.get("/weather")
def weather(city: str):
    return {
        "city": city,
        "temperature": "30°C"
    }

@app.get("/cube/{number}")
def cube(number : int):
    return {
        "number": number,
        "cube": number**3
    }

@app.get("/student/{name}")
def student(name: str):
    return {
        "name": name,
        "course": 'Data Science'
    }

@app.get("/calculator")
def calculator(a: int, b:int):
    return{
        "a" : a,
        "b" : b,
        "sum": a+b
    }
