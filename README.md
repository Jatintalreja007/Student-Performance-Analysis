# 🎓 Student Performance Analysis

## Project Overview
End-to-end student performance analytics project using MySQL, FastAPI, Streamlit, Plotly and Power BI.

## Features
- Student performance analysis
- GPA and attendance insights
- Risk level analysis
- Interactive Streamlit dashboard
- FastAPI backend
- Power BI dashboard

## Tech Stack
Python, MySQL, SQL Stored Procedures, FastAPI, Streamlit, Plotly, Pandas, Power BI

## Project Structure
```
api/
dashboard/
sql/
data/
images/
README.md
requirements.txt
.gitignore
```

## Installation
```bash
pip install -r requirements.txt
```

## Run FastAPI
```bash
uvicorn coll_project:app --reload
```

## Run Dashboard
```bash
streamlit run dashboard.py
```

## Database
Import `college_management.sql` into MySQL and update the credentials in `coll_project.py`.

## Project Documentation

## 📷 Project Screenshots

### Data Cleaning
![Data Cleaning](SNAPSHOT_01.png)

### Major-wise Student Distribution
![Major Distribution](SNAPSHOT_02.png)

### GPA Distribution
![GPA Distribution](SNAPSHOT_03.png)

### Gender Distribution
![Gender Distribution](SNAPSHOT_04.png)

### Attendance vs GPA
![Attendance vs GPA](SNAPSHOT_06.png)

### Assignment Submission vs GPA
![Assignment Submission vs GPA](SNAPSHOT_07.png)

### Enrollment Status
![Enrollment Status](SNAPSHOT_08.png)

## Author
Jatin Talreja
