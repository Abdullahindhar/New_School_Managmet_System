import streamlit as st
import pandas as pd
from utils import load_csv, add_student, add_teacher, predict_defaulter

# ---------- Page Config ----------
st.set_page_config(
    page_title="School Management System",
    layout="wide"
)

st.title("🏫 School Management System")

menu = ["Dashboard","Add Student","View Students","Predict Fee Defaulter","Add Teacher","View Teachers"]
choice = st.sidebar.selectbox("Menu", menu)

# ---------- Small Card Style ----------
def small_card(title, value):
    st.markdown(
        f"""
        <div style="
            padding:10px;
            border-radius:10px;
            background:#f1f5f9;
            text-align:center;
            box-shadow:0 2px 6px rgba(0,0,0,0.1);
        ">
            <h5 style="margin:0;color:#1f4e78;">{title}</h5>
            <h3 style="margin:0;">{value}</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- Dashboard ----------
if choice == "Dashboard":
    students = load_csv("students.csv", ["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"])
    teachers = load_csv("teachers.csv", ["ID","Name","Subjects"])
    classes = load_csv("classes.csv", ["ID","ClassName"])

    # ---- Small Cards ----
    col1, col2, col3 = st.columns(3)
    with col1:
        small_card("Total Students", len(students))
    with col2:
        small_card("Total Teachers", len(teachers))
    with col3:
        small_card("Total Classes", len(classes))

    st.markdown("---")

    # ---- Front Buttons ----
    st.subheader("⚡ Quick Actions")
    b1, b2, b3 = st.columns(3)

    if b1.button("➕ Add Student"):
        st.session_state.page = "Add Student"

    if b2.button("📋 View Students"):
        st.session_state.page = "View Students"

    if b3.button("💰 Predict Fee Defaulter"):
        st.session_state.page = "Predict Fee Defaulter"

    st.markdown("---")

    # ---- Recent Defaulters ----
    st.subheader("🚨 Recent Fee Defaulters")
    if not students.empty:
        students["PaymentRatio"] = students["LastPaid"] / students["TotalFee"]
        defaulters = students[students["PaymentRatio"] < 0.8]

        if not defaulters.empty:
            st.dataframe(defaulters[["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"]])
        else:
            st.success("No fee defaulters 🎉")
    else:
        st.info("No students data available")

# ---------- Add Student ----------
elif choice == "Add Student" or st.session_state.get("page") == "Add Student":
    st.subheader("➕ Add New Student")
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
elif choice == "View Students" or st.session_state.get("page") == "View Students":
    st.subheader("📋 All Students")
    students = load_csv("students.csv", ["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"])
    if not students.empty:
        st.dataframe(students)
    else:
        st.info("No students data available")

# ---------- Predict Fee Defaulter ----------
elif choice == "Predict Fee Defaulter" or st.session_state.get("page") == "Predict Fee Defaulter":
    st.subheader("💰 Predict Fee Defaulter")
    attendance = st.number_input("Attendance (%)", min_value=0, max_value=100)
    last_paid = st.number_input("Last Month Paid")
    total_fee = st.number_input("Total Fee")

    if st.button("Predict"):
        result = predict_defaulter(attendance, last_paid, total_fee)
        st.success(f"Prediction: {result}")

# ---------- Add Teacher ----------
elif choice == "Add Teacher":
    st.subheader("➕ Add New Teacher")
    name = st.text_input("Teacher Name")
    subjects = st.text_input("Subjects (comma separated)")

    if st.button("Add Teacher"):
        add_teacher(name, subjects)
        st.success(f"Teacher {name} added!")

# ---------- View Teachers ----------
elif choice == "View Teachers":
    st.subheader("📋 All Teachers")
    teachers = load_csv("teachers.csv", ["ID","Name","Subjects"])
    if not teachers.empty:
        st.dataframe(teachers)
    else:
        st.info("No teacher data available")
