import streamlit as st
import pandas as pd
import os
from datetime import date

# File to store data
DATA_FILE = "student_records.csv"

# Function to load or create the data file
def load_data():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=["ID", "Name", "Class", "DOB", "Parent Contact", "Status"])
        df.to_csv(DATA_FILE, index=False)
        return df
    return pd.read_csv(DATA_FILE, dtype={"ID": str})

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# --- UI Layout ---
st.set_page_config(page_title="Student Management System", layout="wide")
st.title("🎓 Student Records Executive Portal")

menu = ["View Students", "Add Student", "Update/Upgrade Student", "Remove Student"]
choice = st.sidebar.selectbox("Navigation", menu)

df = load_data()

# 1. VIEW ALL STUDENTS
if choice == "View Students":
    st.subheader("Current Student Directory")
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No records found.")

# 2. ADD STUDENT
elif choice == "Add Student":
    st.subheader("Register New Student")
    with st.form("add_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name")
            student_id = st.text_input("ID Number")
            student_class = st.selectbox("Class", ["Grade 1", "Grade 2", "Grade 3", "Other"])
        with col2:
            dob = st.date_input("Date of Birth", min_value=date(2000, 1, 1))
            contact = st.text_input("Parent's Contact")
        
        submit = st.form_submit_button("Register Student")
        
        if submit:
            if student_id in df['ID'].astype(str).values:
                st.error("This ID already exists!")
            else:
                new_data = pd.DataFrame([[student_id, name, student_class, str(dob), contact, "Active"]], 
                                        columns=df.columns)
                df = pd.concat([df, new_data], ignore_index=True)
                save_data(df)
                st.success(f"Student {name} added successfully!")

# 3. UPDATE / UPGRADE
elif choice == "Update/Upgrade Student":
    st.subheader("Modify Student Information")
    if not df.empty:
        student_to_update = st.selectbox("Select Student by ID", df['ID'].tolist())
        idx = df[df['ID'] == student_to_update].index[0]
        
        with st.form("update_form"):
            new_class = st.text_input("Update Class", value=str(df.at[idx, 'Class']))
            new_contact = st.text_input("Update Parent Contact", value=str(df.at[idx, 'Parent Contact']))
            
            if st.form_submit_button("Apply Changes"):
                df.at[idx, 'Class'] = new_class
                df.at[idx, 'Parent Contact'] = new_contact
                save_data(df)
                st.success("Record updated!")
                st.rerun()
    else:
        st.warning("No records available to update.")

# 4. REMOVE STUDENT
elif choice == "Remove Student":
    st.subheader("Remove Student Record")
    if not df.empty:
        student_to_remove = st.selectbox("Select Student ID to Delete", df['ID'].tolist())
        if st.button("Delete Permanently", type="primary"):
            df = df[df['ID'] != str(student_to_remove)]
            save_data(df)
            st.warning(f"Record {student_to_remove} has been removed.")
            st.rerun()
    else:
        st.info("No records to remove.")