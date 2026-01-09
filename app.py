import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from utils import load_csv, add_student, add_teacher, predict_defaulter

# ---------------- Page Config ----------------
st.set_page_config(
    page_title="School Management System",
    layout="wide"
)

# ---------------- Custom CSS (Streamlit Safe) ----------------
st.markdown("""
<style>
.stApp {
    background-color: #eef3f9;
}

.card {
    background-color: white;
    padding: 20px;
    border-radius: 16px;
    box-shadow: 0 6px 14px rgba(0,0,0,0.12);
    text-align: center;
}

.card:hover {
    transform: scale(1.03);
}

h1, h2, h3, h4 {
    color: #1f4e78;
}

button[kind="primary"] {
    background-color: #1f4e78 !important;
    border-radius: 12px;
    height: 3em;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- Header ----------------
st.markdown("<h1 style='text-align:center;'>🏫 School Management System Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<hr>", unsafe_allow_html=True)

# ---------------- Load Data ----------------
students = load_csv("students.csv", ["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"])
teachers = load_csv("teachers.csv", ["ID","Name","Subjects"])
classes = load_csv("classes.csv", ["ID","ClassName"])

# ---------------- Metrics ----------------
with st.container():
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"<div class='card'><h4>Total Students</h4><h2>{len(students)}</h2></div>", unsafe_allow_html=True)

    with c2:
        st.markdown(f"<div class='card'><h4>Total Teachers</h4><h2>{len(teachers)}</h2></div>", unsafe_allow_html=True)

    with c3:
        st.markdown(f"<div class='card'><h4>Total Classes</h4><h2>{len(classes)}</h2></div>", unsafe_allow_html=True)

    if not students.empty:
        students["PaymentRatio"] = students["LastPaid"] / students["TotalFee"]
        defaulters = students[students["PaymentRatio"] < 0.8]
    else:
        defaulters = []

    with c4:
        st.markdown(f"<div class='card'><h4>Fee Defaulters</h4><h2>{len(defaulters)}</h2></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------------- Dashboard Buttons ----------------
with st.container():
    b1, b2, b3, b4 = st.columns(4)

    if b1.button("➕ Add Student", type="primary"):
        st.session_state.page = "add_student"

    if b2.button("📋 View Students", type="primary"):
        st.session_state.page = "view_students"

    if b3.button("💰 Predict Fee", type="primary"):
        st.session_state.page = "predict_fee"

    if b4.button("👨‍🏫 Add Teacher", type="primary"):
        st.session_state.page = "add_teacher"

st.markdown("<hr>", unsafe_allow_html=True)

page = st.session_state.get("page", "dashboard")

# ---------------- Dashboard Charts ----------------
if page == "dashboard":
    if not students.empty:
        colA, colB = st.columns(2)

        with colA:
            st.subheader("Fee Payment Status")
            fig1, ax1 = plt.subplots()
            ax1.pie(
                [len(defaulters), len(students) - len(defaulters)],
                labels=["Defaulters", "On-Time"],
                autopct="%1.1f%%",
                colors=["#d32f2f", "#2ca02c"]
            )
            st.pyplot(fig1)

        with colB:
            st.subheader("Class-wise Students")
            class_count = students["Class"].value_counts()
            fig2, ax2 = plt.subplots()
            sns.barplot(x=class_count.index, y=class_count.values, ax=ax2)
            ax2.set_xlabel("Class")
            ax2.set_ylabel("Students")
            st.pyplot(fig2)
    else:
        st.info("No data available")

# ---------------- Add Student ----------------
elif page == "add_student":
    st.subheader("➕ Add New Student")
    name = st.text_input("Name")
    class_name = st.text_input("Class")
    attendance = st.number_input("Attendance (%)", 0, 100)
    last_paid = st.number_input("Last Paid Fee")
    total_fee = st.number_input("Total Fee")
    fine = st.number_input("Fine")

    if st.button("Save Student", type="primary"):
        add_student(name, class_name, attendance, last_paid, total_fee, fine)
        st.success("Student added successfully")
        st.session_state.page = "dashboard"

# ---------------- View Students ----------------
elif page == "view_students":
    st.subheader("📋 Students List")
    if not students.empty:
        st.dataframe(students)
    else:
        st.info("No students data")

# ---------------- Predict Fee ----------------
elif page == "predict_fee":
    st.subheader("💰 Fee Defaulter Prediction")
    attendance = st.number_input("Attendance (%)", 0, 100)
    last_paid = st.number_input("Last Paid Fee")
    total_fee = st.number_input("Total Fee")

    if st.button("Predict", type="primary"):
        result = predict_defaulter(attendance, last_paid, total_fee)
        st.success(result)

# ---------------- Add Teacher ----------------
elif page == "add_teacher":
    st.subheader("👨‍🏫 Add Teacher")
    name = st.text_input("Teacher Name")
    subjects = st.text_input("Subjects")

    if st.button("Save Teacher", type="primary"):
        add_teacher(name, subjects)
        st.success("Teacher added successfully")
        st.session_state.page = "dashboard"
