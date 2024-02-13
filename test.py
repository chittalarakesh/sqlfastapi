# Import necessary modules
from fastapi import FastAPI, HTTPException
import sqlite3
from pydantic import BaseModel

# Create a FastAPI instance
app = FastAPI()


# Function to connect to SQLite database
def connect_db():
    return sqlite3.connect('my_database.db')


# Function to create table in the database
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Students
                      (id INTEGER PRIMARY KEY, name TEXT, age INTEGER)''')
    conn.commit()
    conn.close()

create_table()


# Function to fetch all students from the database
def fetch_all_students(name):
    conn = connect_db()
    cursor = conn.cursor()
    query="SELECT * FROM Students"
    cursor.execute(query)

    students = cursor.fetchall()
    conn.close()
    return students


# Function to add a student to the database
def add_student_to_db(name, age):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Students (name, age) VALUES (?, ?)", (name, age))
    conn.commit()
    conn.close()

def update_student_to_db(id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "UPDATE Students SET name = ? WHERE id = ?"
    cursor.execute(query,("Rakesh",id))
    conn.commit()
    conn.close()

def delete_student_to_db(id):
    conn = connect_db()
    cursor = conn.cursor()
    query = "DELETE FROM Students WHERE id = ?"
    cursor.execute(query,(id,))
    conn.commit()
    conn.close()
    
# API to retrieve all students
@app.get("/Students")
async def get_students(name:str="Rakesh"):
    students = fetch_all_students(name)
    if not students:
        raise HTTPException(status_code=404, detail="No students found")
    return {"students": students}


class Student(BaseModel):
    name:str
    age:int

# API to add a student
@app.post("/Students/{name}/{age}")
async def add_student(name: str, age: int):
    add_student_to_db(name, age)
    return {"message": "Student added successfully"}


@app.put("/Students/{id}")
async def update_student(id:int):
    update_student_to_db(id,)
    return {"message": "Student updated successfully"}


@app.delete("/Students/{id}")
async def delete_student(id:int):
    delete_student_to_db(id)
    return {"message": "Student Deleted successfully"}