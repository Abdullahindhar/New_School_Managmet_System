import streamlit as st
import pandas as pd
from utils import load_csv, add_student, add_teacher, predict_defaulter

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="School Management System",
    layout="wide"
)

# ---------------- THEME TOGGLE ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

st.button("🌗 Dark / Light Mode", on_click=toggle_theme)

# ---------------- CUSTOM CSS ----------------
if st.session_state.theme == "dark":
    st.markdown("""
    <style>
        .stApp {background-color: #0e1117; color:white;}
        table {color:white;}
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
        .stApp {background-color: #eef3f9; color:black;}
        table {color:black;}
    </style>
    """, unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
students = load_csv("students.csv", ["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"])
teachers = load_csv("teachers.csv", ["ID","Name","Subjects"])
classes = load_csv("classes.csv", ["ID","ClassName"])

# ---------------- HEADER ----------------
st.markdown("""
<h1 style='text-align:center; color:#1f4e78;'>🏫 School Management System</h1>
<p style='text-align:center;'>Smart Dashboard Overview</p>
<hr>
""", unsafe_allow_html=True)

# ---------------- DASHBOARD CARDS ----------------
col1, col2, col3, col4 = st.columns(4)

def card(title, value, color="#1f77b4"):
    st.markdown(f"""
    <div style='
        background-color:{color}; 
        padding:20px; 
        border-radius:16px; 
        text-align:center;
        color:white;
        font-weight:bold;
        font-size:18px;
        margin-bottom:10px;
    '>
        <h4>{title}</h4>
        <h2>{value}</h2>
    </div>
    """, unsafe_allow_html=True)

card("Total Students", len(students), "#1f77b4")
card("Total Teachers", len(teachers), "#2ca02c")
card("Total Classes", len(classes), "#ff7f0e")
defaulters = students[students["LastPaid"]/students["TotalFee"]<0.8] if not students.empty else []
card("Fee Defaulters", len(defaulters), "#d32f2f")

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- DASHBOARD BUTTONS ----------------
b1, b2, b3, b4, b5 = st.columns(5)

if b1.button("➕ Add Student"):
    st.session_state.page = "add_student"

if b2.button("📘 View Students"):
    st.session_state.page = "view_students"

if b3.button("➕ Add Teacher"):
    st.session_state.page = "add_teacher"

if b4.button("📗 View Teachers"):
    st.session_state.page = "view_teachers"

if b5.button("📊 Analytics"):
    st.session_state.page = "analytics"

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- PAGES ----------------

# ---------- DASHBOARD ----------
if st.session_state.page == "dashboard":
    st.subheader("📌 Recent Fee Defaulters")
    if not defaulters.empty:
        st.dataframe(defaulters[["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"]], use_container_width=True)
    else:
        st.info("No fee defaulters!")

# ---------- ADD STUDENT ----------
elif st.session_state.page == "add_student":
    st.subheader("➕ Add New Student")
    name = st.text_input("Student Name")
    class_name = st.text_input("Class")
    attendance = st.number_input("Attendance (%)", 0, 100)
    last_paid = st.number_input("Last Paid Fee")
    total_fee = st.number_input("Total Fee")
    fine = st.number_input("Fine")

    if st.button("Save Student"):
        add_student(name, class_name, attendance, last_paid, total_fee, fine)
        st.success("✅ Student added successfully")

# ---------- VIEW STUDENTS ----------
elif st.session_state.page == "view_students":
    st.subheader("📘 Students List")
    st.dataframe(students, use_container_width=True)

# ---------- ADD TEACHER ----------
elif st.session_state.page == "add_teacher":
    st.subheader("➕ Add New Teacher")
    name = st.text_input("Teacher Name")
    subjects = st.text_input("Subjects")
    if st.button("Save Teacher"):
        add_teacher(name, subjects)
        st.success("✅ Teacher added successfully")

# ---------- VIEW TEACHERS ----------
elif st.session_state.page == "view_teachers":
    st.subheader("📗 Teachers List")
    st.dataframe(teachers, use_container_width=True)

# ---------- ANALYTICS ----------
elif st.session_state.page == "analytics":
    st.subheader("📊 Analytics Overview")

    colA, colB = st.columns(2)
    with colA:
        st.write("Students per Class")
        st.bar_chart(students["Class"].value_counts())

    with colB:
        st.write("Attendance Distribution")
        st.line_chart(students["Attendance"])

# ---------------- FOOTER ----------------
st.markdown("""
<hr>
<div style="text-align:center; padding:10px; font-size:14px;">
© 2026 <b>School Management System</b> | Developed by <b>Abdullah Indhar</b> 🚀
</div>
""", unsafe_allow_html=True)
