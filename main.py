from fastapi import FastAPI, Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from uuid import UUID

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

############ POST ###################

class Book(BaseModel):
    title: str
    author: str
    pages: int

@app.post("/book")
def create_book(book: Book):
    return {
        "message": "Book received!",
        "book": book
    }


class Student(BaseModel):
    name: str
    age: int
    course: str
    gpa: float

@app.post("/create-student")
def create_student(student: Student):
    return {
        "message": "Student registered.",
        "student": student
    }

''''
Reject Extra fields

from pydantic import BaseModel, ConfigDict

class Student(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    age: int
    course: str
    gpa: float

'''

############# Response model ################
class StudentCreate2(BaseModel):
    name: str
    age: int
    course: str
    gpa: float


class StudentResponse(BaseModel):
    name: str
    course: str


@app.post("/create-student2", response_model=StudentResponse)
def create_student2(student: StudentCreate2):
    return student

########## Validation ##########
'''
name: str = Field(min_length=2, max_length=50)
character will be min - 2 & max - 50 characters
'''

class StudentCreate3(BaseModel):
    name: str = Field(min_length=2, max_length=50) # Min Char 2 - Max Char 50
    age: int = Field(gt=0, lt=120) # should be greater than 0, less than 120
    course: str = Field(min_length=2) # min char 2
    gpa: float = Field(ge=0.0, le=10.0) # gpa range 0-10.


@app.post("/create-student3", response_model=StudentResponse)
def create_student2(student: StudentCreate3):
    return student

### Richer Validations 
'''
from pydantic import EmailStr

email: EmailStr

now - a will fail but a@xyz.com will pass


2. from uuid import UUID
    id: UUID
    only valid uuid will pass.

3. from datetime import datetime

    created_at : datetime

    Only valid datetime strings.
'''

################ Status Codes ################
'''
| Code | Meaning               | Example                             |
| ---- | --------------------- | ----------------------------------- |
| 200  | OK                    | Successfully fetched data           |
| 201  | Created               | Successfully created a resource     |
| 204  | No Content            | Deleted successfully                |
| 400  | Bad Request           | Invalid request from client         |
| 401  | Unauthorized          | Not logged in / invalid credentials |
| 403  | Forbidden             | Logged in but not allowed           |
| 404  | Not Found             | Resource doesn't exist              |
| 409  | Conflict              | Duplicate resource                  |
| 422  | Unprocessable Entity  | Validation failed                   |
| 500  | Internal Server Error | Something broke on the server       |

'''

from fastapi import FastAPI, status

@app.post(
    "/create-student",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_student(student: StudentCreate3):
    return student


########### HTTP Exception ###########
from fastapi import HTTPException

@app.get("/students/{student_id}")
def get_student(student_id: int):
    if student_id != 1:
        raise HTTPException(
            status_code=404,
            detail='Student not found.'
        )
    return {
        "id": 1,
        "Name": 'Pratik',
        "Course": 'Data Science'

    }

# raised - http exceptions

########## Dependency Injection ############
from fastapi import Depends

def get_app_name():
    return "FastAPI Learning"

@app.get("/info")
def info(app_name = Depends(get_app_name)):
    return {
        "application": app_name
    }

'''
FastAPI calls the dependency function before the endpoint function, then injects (passes) its return value into the endpoint parameter.

bts : it's doing : -> app = get_app_name() then info(app)
'''