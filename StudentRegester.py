import streamlit as st
import mysql.connector
from mysql.connector import Error
import re

# Database connection function
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="82.180.143.66",
            user="u263681140_AttendanceInt",
            password="SagarAtten@12345",
            database="u263681140_Attendance"
        )
        return conn
    except Error as e:
        st.error(f"Error connecting to MySQL: {e}")
        return None

# Duplicate check function
def is_duplicate(conn, email, mobile):
    cursor = conn.cursor()
    query = """
        SELECT Email, Mobile FROM Students_Data
        WHERE Email = %s OR Mobile = %s
    """
    cursor.execute(query, (email, mobile))
    result = cursor.fetchone()
    cursor.close()
    return result

# Validation functions
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_mobile(mobile):
    return re.match(r"^\d{10}$", mobile)

# Insert data function
def insert_student_data(student_name, college, batch, mobile, email, address):
    conn = create_connection()
    if conn:
        duplicate = is_duplicate(conn, email, mobile)
        if duplicate:
            existing_email, existing_mobile = duplicate
            if email == existing_email:
                st.error("❌ Email already registered.")
            elif mobile == existing_mobile:
                st.error("❌ Mobile number already registered.")
        else:
            cursor = conn.cursor()
            query = """
                INSERT INTO Students_Data (StudentName, StudentCollege, Batch, Mobile, Email, Address)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (student_name, college, batch, mobile, email, address)
            try:
                cursor.execute(query, values)
                conn.commit()
                st.success("✅ Student registered successfully!")
            except Error as e:
                st.error(f"❌ Failed to insert record: {e}")
            finally:
                cursor.close()
                conn.close()

# Streamlit form
st.title("📋 Student Attendance Registration")

with st.form("register_form"):
    student_name = st.text_input("Student Name")
    
    college_options = ["GP Malvan", "GP Karad", "GP Kolhapur", "AIT Vita", "Jayawantrao Bhosale Poly K.M.", "Other"]
    college = st.selectbox("Select College", college_options)
    
    batch_options = ["B1", "B2"]
    batch = st.selectbox("Select Batch", batch_options)
    
    mobile = st.text_input("Mobile")
    email = st.text_input("Email")
    address = st.text_area("Address")
    
    submitted = st.form_submit_button("Register")

    if submitted:
        if not all([student_name, college, batch, mobile, email, address]):
            st.warning("⚠️ Please fill all the fields.")
        elif not is_valid_mobile(mobile):
            st.error("❌ Invalid mobile number. Please enter a 10-digit number.")
        elif not is_valid_email(email):
            st.error("❌ Invalid email address format.")
        else:
            insert_student_data(student_name, college, batch, mobile, email, address)
