import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# ---------------------------------
# PAGE CONFIG
# ---------------------------------
st.set_page_config(page_title="Student Analytics Dashboard", layout="wide")

st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'>🎓 Student Analytics Dashboard</h1>",
    unsafe_allow_html=True
)

# ---------------------------------
# API URL
# ---------------------------------
api_url = "http://127.0.0.1:8000/students_Management"

# ---------------------------------
# FETCH DATA
# ---------------------------------
try:
    response = requests.get(api_url)
    response.raise_for_status()
    json_data = response.json()
    data = json_data["data"] if "data" in json_data else json_data
    df = pd.DataFrame(data)

except Exception as e:
    st.error(f"API Connection Error: {e}")
    st.stop()

# ---------------------------------
# CONVERT NUMERIC COLUMNS
# ---------------------------------
numeric_columns = [
    'GPA',
    'attendance_rate',
    'assignment_submission_rate',
    'avg_session_duration_minutes'
]

for col in numeric_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

# ---------------------------------
# SIDEBAR FILTERS
# ---------------------------------
st.sidebar.header("🔎 Filters")

if 'major' in df.columns:
    major_filter = st.sidebar.selectbox(
        "Select Major",
        ["All"] + sorted(df['major'].dropna().unique())
    )
else:
    major_filter = "All"

if 'risk_level' in df.columns:
    risk_filter = st.sidebar.selectbox(
        "Select Risk Level",
        ["All"] + sorted(df['risk_level'].dropna().unique())
    )
else:
    risk_filter = "All"

if major_filter != "All":
    df = df[df['major'] == major_filter]

if risk_filter != "All":
    df = df[df['risk_level'] == risk_filter]

# ---------------------------------
# KPI SECTION
# ---------------------------------
st.markdown("## 📊 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Students", df['student_id'].nunique())
col2.metric("Average CGPA", round(df['GPA'].mean(), 2))
col3.metric("High Risk Students", df[df['risk_level']=="High"].shape[0])
col4.metric("Active Students", df[df['enrollment_status']=="Active"].shape[0])

st.markdown("---")

# ---------------------------------
# CHARTS ROW 1
# ---------------------------------
col1, col2 = st.columns(2)

# Students per Major
with col1:
    st.subheader("Students per Major")
    major_counts = df['major'].value_counts().reset_index()
    major_counts.columns = ['major', 'count']
    fig1 = px.bar(
        major_counts,
        x='major',
        y='count',
        color='count',
        template='plotly_white',
        title="Students per Major"
    )
    st.plotly_chart(fig1, use_container_width=True)

# Risk Distribution
with col2:
    st.subheader("Risk Level Distribution")
    risk_counts = df['risk_level'].value_counts().reset_index()
    risk_counts.columns = ['risk_level', 'count']
    fig2 = px.pie(
        risk_counts,
        names='risk_level',
        values='count',
        hole=0.4,
        template='plotly_white',
        title="Risk Level Distribution"
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ---------------------------------
# CHARTS ROW 2
# ---------------------------------
col1, col2 = st.columns(2)

# Average GPA per Major
with col1:
    st.subheader("Average GPA per Major")
    gpa_major = df.groupby('major')['GPA'].mean().reset_index()
    fig3 = px.line(
        gpa_major,
        x='major',
        y='GPA',
        markers=True,
        template='plotly_white',
        title="Average GPA per Major"
    )
    st.plotly_chart(fig3, use_container_width=True)

# GPA Distribution
with col2:
    st.subheader("GPA Distribution")
    fig4 = px.histogram(
        df,
        x='GPA',
        nbins=20,
        template='plotly_white',
        title="GPA Distribution"
    )
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# ---------------------------------
# CHARTS ROW 3
# ---------------------------------

# Attendance vs GPA
# ---------------------------------
# Attendance vs GPA (Scatter Chart)
# ---------------------------------

st.subheader("Attendance vs GPA Analysis")

if 'attendance_rate' in df.columns and 'GPA' in df.columns:

    fig5 = px.scatter(
        df,
        x='attendance_rate',
        y='GPA',
        color='risk_level' if 'risk_level' in df.columns else None,
        size='lms_logins_past_month' if 'lms_logins_past_month' in df.columns else None,
        hover_data=['student_id', 'major'] if 'student_id' in df.columns else None,
        template='plotly_white',
        title="Attendance vs GPA"
    )

    st.plotly_chart(fig5, use_container_width=True)

else:
    st.write("Required columns not found for scatter plot.")


st.markdown("---")

# Assignment Submission by Risk
st.subheader("Assignment Submission Rate by Risk Level")
assignment_risk = df.groupby('risk_level')['assignment_submission_rate'].mean().reset_index()
fig6 = px.bar(
    assignment_risk,
    x='risk_level',
    y='assignment_submission_rate',
    template='plotly_white',
    title="Avg Assignment Submission by Risk"
)
st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# Data Table
st.subheader("📄 Detailed Data")
st.dataframe(df, use_container_width=True)
