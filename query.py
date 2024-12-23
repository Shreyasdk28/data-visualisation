import mysql.connector

# Database connection setup
try:
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="shreyas",
        db="streamlit_project"
    )
    print("Connection successful!")
    
    # Create a cursor to interact with the database
    cursor = conn.cursor()
    print("Cursor created.")
    
    # Execute the SQL query
    cursor.execute("SELECT * FROM insurance")
    print("Query executed.")
    
    # Fetch the data
    result = cursor.fetchall()
    print("Data fetched:", result)

except mysql.connector.Error as e:
    print(f"Connection failed: {e}")

finally:
    if conn.is_connected():
        conn.close()
        print("Connection closed.")


# conn=mysql.connector.connect(
#     host="localhost",
#     port="3306",
#     user="root",
#     password="shreyas",
#     db="streamlit_project"
# )
# c=conn.cursor()

#fetch

# def view_all_data():
#     c.execute("select * from insurance order by id asc")
#     data=c.fetchall()
#     return data


    
    

# conn=mysql.connector.connect(
#     host="localhost",
#     port="3306",
#     user="root",
#     password="shreyas",
#     db="streamlit_project"
# )
# c=conn.cursor()

#fetch

# def view_all_data():
#     c.execute("select * from insurance order by id asc")
#     data=c.fetchall()
#     return data


def view_all_data():
    # Example function implementation
    return [
        (1, "2024-12-31", "New York", "NY", "Northeast", 1000000, "Concrete", "Retail", True, False, "A", 101),
        (2, "2025-01-15", "Los Angeles", "CA", "West", 2000000, "Wood", "Residential", False, True, "B", 102),
        # Add more rows as needed
    ]
