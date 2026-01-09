import streamlit as st
import pandas as pd
from utils import load_csv, add_student, add_teacher, predict_defaulter

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="School Management System",
    layout="wide"
)

# ---------------- THEME ----------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

def toggle_theme():
    st.session_state.theme = "dark" if st.session_state.theme == "light" else "light"

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
/* Body background */
.stApp {
    background: linear-gradient(to right, #e0f7fa, #fff3e0);
}

/* Header buttons */
.button-header {
    background-color:#1f77b4; color:white; border:none;
    padding:10px 20px; border-radius:12px;
    font-weight:bold; margin-right:10px; cursor:pointer;
}
.button-header:hover {
    background-color:#155a8a;
}

/* Cards */
.card {
    background-color:#2ca02c;
    color:white;
    padding:15px;
    border-radius:15px;
    text-align:center;
    font-weight:bold;
    margin-bottom:15px;
    box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
}
.card:hover {
    transform: scale(1.05);
    transition: 0.3s;
}

/* Footer */
footer {
    text-align:center;
    font-size:14px;
    padding:10px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
students = load_csv("students.csv", ["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"])
teachers = load_csv("teachers.csv", ["ID","Name","Subjects"])
classes = load_csv("classes.csv", ["ID","ClassName"])
defaulters = students[students["LastPaid"]/students["TotalFee"]<0.8] if not students.empty else []

# ---------------- HEADER ----------------
st.markdown("<h1 style='text-align:center; color:#1f4e78;'>🏫 School Management System</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Smart Dashboard Overview</p><hr>", unsafe_allow_html=True)

# ---------------- DASHBOARD BUTTONS ----------------
btn1, btn2, btn3, btn4, btn5 = st.columns(5)

if btn1.button("➕ Add Student", key="btn_add_student"):
    st.session_state.page = "add_student"

if btn2.button("📘 View Students", key="btn_view_student"):
    st.session_state.page = "view_students"

if btn3.button("➕ Add Teacher", key="btn_add_teacher"):
    st.session_state.page = "add_teacher"

if btn4.button("📗 View Teachers", key="btn_view_teacher"):
    st.session_state.page = "view_teachers"

if btn5.button("📊 Analytics", key="btn_analytics"):
    st.session_state.page = "analytics"

if "page" not in st.session_state:
    st.session_state.page = "dashboard"

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- DASHBOARD CARDS ----------------
cards_col1, cards_col2, cards_col3, cards_col4 = st.columns(4)

cards_col1.markdown(f"<div class='card'>Total Students<br><h2>{len(students)}</h2></div>", unsafe_allow_html=True)
cards_col2.markdown(f"<div class='card' style='background-color:#ff7f0e'>Total Teachers<br><h2>{len(teachers)}</h2></div>", unsafe_allow_html=True)
cards_col3.markdown(f"<div class='card' style='background-color:#1f77b4'>Total Classes<br><h2>{len(classes)}</h2></div>", unsafe_allow_html=True)
cards_col4.markdown(f"<div class='card' style='background-color:#d32f2f'>Fee Defaulters<br><h2>{len(defaulters)}</h2></div>", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- PAGES ----------------

# DASHBOARD MAIN
if st.session_state.page == "dashboard":
    st.subheader("📌 Recent Fee Defaulters")
    if not defaulters.empty:
        st.dataframe(defaulters[["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"]], use_container_width=True)
    else:
        st.info("No fee defaulters!")

# ADD STUDENT
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

# VIEW STUDENTS
elif st.session_state.page == "view_students":
    st.subheader("📘 Students List")
    st.dataframe(students, use_container_width=True)

# ADD TEACHER
elif st.session_state.page == "add_teacher":
    st.subheader("➕ Add New Teacher")
    name = st.text_input("Teacher Name")
    subjects = st.text_input("Subjects")
    if st.button("Save Teacher"):
        add_teacher(name, subjects)
        st.success("✅ Teacher added successfully")

# VIEW TEACHERS
elif st.session_state.page == "view_teachers":
    st.subheader("📗 Teachers List")
    st.dataframe(teachers, use_container_width=True)

# ANALYTICS
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
<footer>
© 2026 <b>School Management System</b> | Developed by <b>Abdullah Indhar</b> 🚀
</footer>
""", unsafe_allow_html=True)
