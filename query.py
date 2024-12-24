import mysql.connector
import streamlit as st
import pandas as pd


# Database connection
try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mydb"
    )
    # st.success("Database connected!")
except mysql.connector.Error as e:
    st.error(f"Database connection failed: {e}")
    st.stop()  # Stop execution if the database connection fails

# Fetch data function
def view_all_data():
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM insurance ORDER BY id ASC")
        result = cursor.fetchall()
        return result
    except mysql.connector.Error as e:
        st.error(f"Failed to fetch data: {e}")
        return []

  # This will print the result of the SQL query

view_all_data()



