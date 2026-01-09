import streamlit as st
import pandas as pd
from utils import load_csv, add_student, add_teacher, predict_defaulter

# ---------- Page Config ----------
st.set_page_config(
    page_title="School Management System",
    layout="wide"
)

# ---------- Background + Style ----------
st.markdown("""
<style>
body {
    background-color: #f4f7fb;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    text-align: center;
}
.btn {
    width:100%;
    padding:12px;
    border-radius:10px;
    background:#1f4e78;
    color:white;
    font-size:16px;
    border:none;
}
.btn:hover {
    background:#163a5f;
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("<h1 style='text-align:center;color:#1f4e78;'>🏫 School Management System</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------- Load Data ----------
students = load_csv("students.csv", ["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"])
teachers = load_csv("teachers.csv", ["ID","Name","Subjects"])
classes = load_csv("classes.csv", ["ID","ClassName"])

# ---------- Metrics ----------
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"<div class='card'><h4>Total Students</h4><h2>{len(students)}</h2></div>", unsafe_allow_html=True)
with c2:
    st.markdown(f"<div class='card'><h4>Total Teachers</h4><h2>{len(teachers)}</h2></div>", unsafe_allow_html=True)
with c3:
    st.markdown(f"<div class='card'><h4>Total Classes</h4><h2>{len(classes)}</h2></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- Action Buttons ----------
b1, b2, b3, b4 = st.columns(4)

if b1.button("➕ Add Student"):
    st.session_state.page = "add_student"

if b2.button("📋 View Students"):
    st.session_state.page = "view_students"

if b3.button("💰 Predict Fee"):
    st.session_state.page = "predict_fee"

if b4.button("👨‍🏫 Add Teacher"):
    st.session_state.page = "add_teacher"

st.markdown("<hr>", unsafe_allow_html=True)

# ---------- Pages ----------
page = st.session_state.get("page", "home")

# ---- Add Student ----
if page == "add_student":
    st.subheader("➕ Add Student")
    name = st.text_input("Name")
    class_name = st.text_input("Class")
    attendance = st.number_input("Attendance (%)", 0, 100)
    last_paid = st.number_input("Last Paid")
    total_fee = st.number_input("Total Fee")
    fine = st.number_input("Fine")

    if st.button("Save Student"):
        add_student(name, class_name, attendance, last_paid, total_fee, fine)
        st.success("Student Added Successfully")

# ---- View Students ----
elif page == "view_students":
    st.subheader("📋 Students List")
    if not students.empty:
        st.dataframe(students)
    else:
        st.info("No student data")

# ---- Predict Fee ----
elif page == "predict_fee":
    st.subheader("💰 Fee Defaulter Prediction")
    attendance = st.number_input("Attendance (%)", 0, 100)
    last_paid = st.number_input("Last Paid")
    total_fee = st.number_input("Total Fee")

    if st.button("Predict"):
        result = predict_defaulter(attendance, last_paid, total_fee)
        st.success(result)

# ---- Add Teacher ----
elif page == "add_teacher":
    st.subheader("👨‍🏫 Add Teacher")
    name = st.text_input("Teacher Name")
    subjects = st.text_input("Subjects")

    if st.button("Save Teacher"):
        add_teacher(name, subjects)
        st.success("Teacher Added")
