import pandas as pd
import os
import joblib
from sklearn.ensemble import RandomForestClassifier

# ---------- File Paths ----------
STUDENT_FILE = "students.csv"
TEACHER_FILE = "teachers.csv"
CLASS_FILE = "classes.csv"
MODEL_FILE = "fee_defaulter_model.pkl"

# ---------- Load CSV ----------
def load_csv(file_path, columns):
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        df = pd.DataFrame(columns=columns)
        df.to_csv(file_path, index=False)
        return df

# ---------- Save CSV ----------
def save_csv(df, file_path):
    df.to_csv(file_path, index=False)

# ---------- Add Student ----------
def add_student(name, class_name, attendance, last_paid, total_fee, fine):
    df = load_csv(STUDENT_FILE, ["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"])
    new_id = 1 if df.empty else df["ID"].max() + 1
    df = pd.concat([df, pd.DataFrame([{
        "ID": new_id,
        "Name": name,
        "Class": class_name,
        "Attendance": attendance,
        "LastPaid": last_paid,
        "TotalFee": total_fee,
        "Fine": fine
    }])], ignore_index=True)
    save_csv(df, STUDENT_FILE)

# ---------- Add Teacher ----------
def add_teacher(name, subjects):
    df = load_csv(TEACHER_FILE, ["ID","Name","Subjects"])
    new_id = 1 if df.empty else df["ID"].max() + 1
    df = pd.concat([df, pd.DataFrame([{
        "ID": new_id,
        "Name": name,
        "Subjects": subjects
    }])], ignore_index=True)
    save_csv(df, TEACHER_FILE)

# ---------- Train Model ----------
def train_model():
    df = load_csv(STUDENT_FILE, ["ID","Name","Class","Attendance","LastPaid","TotalFee","Fine"])
    if df.empty:
        print("No student data to train.")
        return None
    # Simple feature: Attendance + LastPaid/TotalFee
    X = df[["Attendance","LastPaid","TotalFee"]]
    X["PaymentRatio"] = X["LastPaid"]/X["TotalFee"]
    y = X["PaymentRatio"].apply(lambda x: 1 if x<0.8 else 0)  # 1=Defaulter, 0=OnTime
    clf = RandomForestClassifier()
    clf.fit(X[["Attendance","LastPaid","TotalFee","PaymentRatio"]], y)
    joblib.dump(clf, MODEL_FILE)
    print("Model trained and saved!")
    return clf

# ---------- Predict Defaulter ----------
def predict_defaulter(attendance, last_paid, total_fee):
    if not os.path.exists(MODEL_FILE):
        clf = train_model()
    else:
        clf = joblib.load(MODEL_FILE)
    X = pd.DataFrame([{
        "Attendance": attendance,
        "LastPaid": last_paid,
        "TotalFee": total_fee,
        "PaymentRatio": last_paid/total_fee
    }])
    pred = clf.predict(X)[0]
    return "⚠️ Defaulter" if pred==1 else "✅ On Time"