from fastapi import FastAPI
import mysql.connector

app = FastAPI()

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="System",
    database="coll_project"
)

@app.get("/")
def home():
    return {"message": "My College API is running 🚀"}

@app.get("/students_Management")
def get_students_management():
    cursor = db.cursor(dictionary=True)
    cursor.callproc('GetFullStudentReport')

    data = []
    for result in cursor.stored_results():
        data = result.fetchall()

    return data