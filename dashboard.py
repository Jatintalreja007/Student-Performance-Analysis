import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Student Analytics Dashboard", layout="wide")

st.markdown("""
<h1 style='text-align: center; color: #2E86C1;'>🎓 Student Analytics Dashboard</h1>
""", unsafe_allow_html=True)

# ---------------------------------
# API URL
# ---------------------------------
api_url = "http://127.0.0.1:8000/students_Management"

# ---------------------------------
# FETCH DATA (FIXED)
# ---------------------------------
try:
    response = requests.get(api_url)
    response.raise_for_status()
    json_data = response.json()

    # Handle both formats
    if isinstance(json_data, dict) and "data" in json_data:
        df = pd.DataFrame(json_data["data"])
    else:
        df = pd.DataFrame(json_data)

except Exception as e:
    st.error(f"API Error: {e}")
    st.stop()

# ---------------------------------
# DATA CLEANING
# ---------------------------------
numeric_cols = [
    'GPA', 'attendance_rate', 'assignment_submission_rate',
    'avg_session_duration_minutes', 'lms_logins_past_month',
    'video_completion_rate', 'age', 'forum_participation_count'
]

for col in numeric_cols:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
st.sidebar.header("🔎 Filters")

major_filter = st.sidebar.selectbox(
    "Select Major",
    ["All"] + sorted(df['major'].dropna().unique()) if 'major' in df.columns else ["All"]
)

risk_filter = st.sidebar.selectbox(
    "Select Risk Level",
    ["All"] + sorted(df['risk_level'].dropna().unique()) if 'risk_level' in df.columns else ["All"]
)

if major_filter != "All":
    df = df[df['major'] == major_filter]

if risk_filter != "All":
    df = df[df['risk_level'] == risk_filter]

# ---------------------------------
# KPI SECTION (FIXED)
# ---------------------------------
st.markdown("## 📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

total_students = df['student_id'].nunique() if 'student_id' in df.columns else 0
avg_gpa = round(df['GPA'].mean(), 2) if 'GPA' in df.columns else 0
high_risk = df[df['risk_level']=="High"].shape[0] if 'risk_level' in df.columns else 0
active_students = df[df['enrollment_status']=="Active"].shape[0] if 'enrollment_status' in df.columns else 0

col1.metric("Total Students", total_students)
col2.metric("Average GPA", avg_gpa)
col3.metric("High Risk Students", high_risk)
col4.metric("Active Students", active_students)

st.markdown("---")

# ---------------------------------
# CHART 1: Students per Major
# ---------------------------------
if 'major' in df.columns:
    st.subheader("Students per Major")
    fig = px.bar(df, x='major', color='major')
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# CHART 2: Risk Distribution
# ---------------------------------
if 'risk_level' in df.columns:
    st.subheader("Risk Level Distribution")
    fig = px.pie(df, names='risk_level', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---------------------------------
# CHART 3: GPA Distribution
# ---------------------------------
if 'GPA' in df.columns:
    st.subheader("GPA Distribution")
    fig = px.histogram(df, x='GPA', nbins=20)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# CHART 4: Attendance vs GPA
# ---------------------------------
if 'attendance_rate' in df.columns and 'GPA' in df.columns:
    st.subheader("Attendance vs GPA")
    fig = px.scatter(
        df,
        x='attendance_rate',
        y='GPA',
        color='risk_level' if 'risk_level' in df.columns else None,
        size='lms_logins_past_month' if 'lms_logins_past_month' in df.columns else None
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---------------------------------
# CHART 5: Gender Distribution
# ---------------------------------
if 'gender' in df.columns:
    st.subheader("Gender Distribution")
    fig = px.pie(df, names='gender', hole=0.4)
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# CHART 6: Enrollment Status
# ---------------------------------
if 'enrollment_status' in df.columns:
    st.subheader("Enrollment Status")
    fig = px.pie(df, names='enrollment_status', hole=0.5)
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ---------------------------------
# CHART 7: Video Completion vs GPA
# ---------------------------------
if 'video_completion_rate' in df.columns and 'GPA' in df.columns:
    st.subheader("Video Completion vs GPA")
    fig = px.scatter(df, x='video_completion_rate', y='GPA', color='risk_level')
    st.plotly_chart(fig, use_container_width=True)

# ---------------------------------
# CHART 8: Forum Participation
# ---------------------------------
if 'forum_participation_count' in df.columns:
    st.subheader("Forum Participation by Risk")
    fig = px.box(df, x='risk_level', y='forum_participation_count')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")



# ---------------------------------
# FINAL TABLE
# ---------------------------------
st.subheader("📄 Detailed Data")
st.dataframe(df, use_container_width=True)