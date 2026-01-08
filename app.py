import streamlit as st
import pandas as pd
from utils import load_csv, save_csv, add_student, add_teacher, predict_defaulter

st.set_page_config(page_title="School Management System", layout="wide")
st.title("🏫 School Management System")

menu = ["Dashboard","Add Student","View Students","Predict Fee Defaulter","Add Teacher","View Teachers"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------- Dashboard ----------
if choice=="Dashboard":
    students = load_csv("students.csv", ["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"])
    teachers = load_csv("teachers.csv", ["ID","Name","Subjects"])
    classes = load_csv("classes.csv", ["ID","ClassName"])
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", len(students))
    col2.metric("Total Teachers", len(teachers))
    col3.metric("Total Classes", len(classes))
    st.subheader("Recent Fee Defaulters")
    if not students.empty:
        students["PaymentRatio"] = students["LastPaid"]/students["TotalFee"]
        defaulters = students[students["PaymentRatio"]<0.8]
        st.dataframe(defaulters[["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"]])
    else:
        st.info("No students data available")

# ---------- Add Student ----------
elif choice=="Add Student":
    st.subheader("Add New Student")
    name = st.text_input("Name")
    class_name = st.text_input("Class")
    attendance = st.number_input("Attendance (%)", min_value=0, max_value=100)
    last_paid = st.number_input("Last Month Paid")
    total_fee = st.number_input("Total Fee")
    fine = st.number_input("Fine")
    if st.button("Add Student"):
        add_student(name, class_name, attendance, last_paid, total_fee, fine)
        st.success(f"Student {name} added!")

# ---------- View Students ----------
elif choice=="View Students":
    st.subheader("All Students")
    students = load_csv("students.csv", ["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"])
    if not students.empty:
        st.dataframe(students)
    else:
        st.info("No students data available")

# ---------- Predict Fee Defaulter ----------
elif choice=="Predict Fee Defaulter":
    st.subheader("Predict Fee Defaulter")
    attendance = st.number_input("Attendance (%)", min_value=0, max_value=100)
    last_paid = st.number_input("Last Month Paid")
    total_fee = st.number_input("Total Fee")
    if st.button("Predict"):
        result = predict_defaulter(attendance, last_paid, total_fee)
        st.success(f"Prediction: {result}")

# ---------- Add Teacher ----------
elif choice=="Add Teacher":
    st.subheader("Add New Teacher")
    name = st.text_input("Teacher Name")
    subjects = st.text_input("Subjects (comma separated)")
    if st.button("Add Teacher"):
        add_teacher(name, subjects)
        st.success(f"Teacher {name} added!")

# ---------- View Teachers ----------
elif choice=="View Teachers":
    st.subheader("All Teachers")
    teachers = load_csv("teachers.csv", ["ID","Name","Subjects"])
    if not teachers.empty:
        st.dataframe(teachers)
    else:
        st.info("No teacher data available")
