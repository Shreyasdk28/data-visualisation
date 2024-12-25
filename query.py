import streamlit as st

# Database connection
try:
    conn = st.connection('mysql', type='sql')
    # st.success("Database connected!")
except Exception as e:
    st.error(f"Database connection failed: {e}")
    st.stop()  # Stop execution if the database connection fails

# Fetch data function
def view_all_data():
    try:
        query = "SELECT * FROM insurance ORDER BY id ASC"
        result = conn.query(query, ttl=600)  # Cache results for 600 seconds
        # st.write(result)
        return result
    except Exception as e:
        # st.error(f"Failed to fetch data: {e}")
        # st.write("No data found")
        return []

# Display the data
# view_all_data()
