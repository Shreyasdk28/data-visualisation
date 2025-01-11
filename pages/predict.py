import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from query import view_all_data

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")  


theme_plotly = None 

#sidebar
st.sidebar.image("data/logo1.png")

# load Style css
# with open('style.css')as f:
#     st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
# Load the Excel file into a DataFrame
# file_path = 'python_query.xlsx'  
# df = pd.read_excel(file_path)

try:
    df = view_all_data()  # Ensure view_all_data returns a DataFrame
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# with st.expander("🔷 **View Original Dataset | Excel file**"):
#  st.dataframe(df,use_container_width=True)
# Title for the rule-based predictive modeling section
st.title("Predictive Modeling for Claim Approval (Rule-Based)")

# User Inputs with Streamlit widgets
policy = st.text_input("Enter Policy Number:")
expiry = st.date_input("Enter Expiry Date:")
location = st.selectbox("Select Location:", ['Urban', 'Rural'])
state = st.selectbox("Enter State:",df['State'].unique())
region = st.selectbox("Select Region:", df['Region'].unique())
investment = st.number_input("Enter Investment Amount:", min_value=0)
construction = st.selectbox("Select Construction Type:", ['Safe', 'Moderate', 'Risky'])
business_type = st.selectbox("Select Business Type:", ['Small', 'Medium', 'Large'])
earthquake = st.selectbox("Earthquake Risk Level:", ['Low', 'Medium', 'High'])
flood = st.selectbox("Flood Risk Level:", ['Low', 'Medium', 'High'])
rating = st.slider("Enter Rating (1 to 5):", min_value=1, max_value=5)

# Predictive Rule-Based Decision
if st.button("Predict"):
    # Initialize approval as True
    approval = True

    # Define rules for prediction
    if earthquake == 'High' or flood == 'High':  # Rule: High risks
        approval = False

    if construction == 'Safe' and rating >= 4:  # Rule: Safe construction and high rating
        approval = True

    if investment > 500000 and (earthquake == 'Medium' or flood == 'Medium') and construction == 'Risky':  # Rule: Risky investment
        approval = False

    if location == 'Urban' and business_type == 'Large':  # Rule: Urban areas and large businesses
        approval = True

    # Display result with styled metric cards
    st.subheader("Decision Result")
    style_metric_cards()
    if approval:
        st.success(f"✅ Policy **{policy}** is **APPROVED** based on the current conditions.")
    else:
        st.error(f"❌ Policy **{policy}** is **REJECTED** based on the current conditions.")

# Additional styling (optional)
st.markdown("""
    <style>
    .stButton>button {
        background-color: #007BFF;  /* Blue background */
        color: white;               /* White text */
        font-size: 16px;
        border-radius: 10px;
        padding: 10px 20px;
        border: none;               /* Remove border */
    }
    .stButton>button:hover {
        background-color: #0056b3;  /* Darker blue when hovered */
    }
</style>

""", unsafe_allow_html=True)
