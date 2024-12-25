import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards
from query import view_all_data

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")  
st.subheader("PYTHON QUERY OPERATIONS | FETCH DATA FROM DATASET BY ADVANCED QUERY")

theme_plotly = None 

#sidebar
st.sidebar.image("data/logo1.png")

# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
# Load the Excel file into a DataFrame
# file_path = 'python_query.xlsx'  
# df = pd.read_excel(file_path)

try:
    df = view_all_data()  # Ensure view_all_data returns a DataFrame
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

with st.expander("🔷 **View Original Dataset | Excel file**"):
 st.dataframe(df,use_container_width=True)

# TASK 1: Display results using Streamlit metrics cards horizontally
# Query 1
with st.expander("**QUERY 1:** Select count **States** by Frequency"):
 state_count = df['State'].value_counts().reset_index()
 state_count.columns = ['State', 'Frequency']
 st.write("Count of States by Frequency:")
 st.dataframe(state_count,use_container_width=True)

# Bar graph for Query 2
with st.expander("**QUERY 2:** **Pictorial** view of the query 1 using **Simple Bar Graph**"):
 fig3 = px.bar(state_count, x='State', y='Frequency', labels={'x': 'State', 'y': 'Frequency'}, title='Frequency of States') 
#  fig3.update_xaxes(showgrid=True)
#  fig3.update_yaxes(showgrid=True)
 st.plotly_chart(fig3,use_container_width=True)

# Query 3
with st.expander("**QUERY 3:** Select count **BusinessType** by frequency"):
 business_type_count = df['BusinessType'].value_counts().reset_index()
 business_type_count.columns = ['BusinessType', 'Frequency']
 st.write("Count of Business Types by Frequency:")
 st.dataframe(business_type_count,use_container_width=True)

# Bar graph for Query 4
with st.expander("**QUERY 4:** select count **BusinessType**  by frequency and print in dataframe and show simple bar graph with grids and legend"):
 fig4 = px.bar(business_type_count, x='BusinessType', y='Frequency', labels={'x': 'BusinessType', 'y': 'Frequency'}, title='Frequency of Business Types')
 fig4.update_layout(showlegend=True)
 fig4.update_xaxes(showgrid=True)
 fig4.update_yaxes(showgrid=True)
 st.plotly_chart(fig4,use_container_width=True)

# Query 5: Minimum Investment and Rating in Uttar Pradesh within a date range
with st.expander("**QUERY 5:** Select minimal **Investment** and minimal **Rating** where **State** is Uttar Pradesh and Expiry date is in the range 2-Jan-21 to 16-Jan-21"):
    query_5 = df[(df['State'] == 'Uttar Pradesh') & 
                 (df['Expiry'] >= '2021-01-02') & 
                 (df['Expiry'] <= '2021-01-16')][['Investment', 'Rating']].min()
    st.success("Minimum **Investment** and **Rating** where **State** is **Uttar Pradesh** and date is in the specified range:")
    st.dataframe(query_5)

# Query 6: Count of Location in Uttar Pradesh
with st.expander("**QUERY 6:** Select count of **Location** where **State** is 'Uttar Pradesh'"):
    count_location = df[df['State'] == "Uttar Pradesh"]['Location'].count()
    st.info(f"## {count_location}")

# Query 7: Count of Location and Region in Karnataka and East
with st.expander("**QUERY 7:** Select count of **Location** and **Region** where **State** is 'Karnataka' and **Region** is 'East'"):
    count_location_region = df[(df['State'] == "Karnataka") & (df['Region'] == "East")]['Location'].count()
    st.info(f"## {count_location_region:,}")

# Query 8: Count of Location and Region with Investment > 300,000 in Karnataka and East
with st.expander("**QUERY 8:** Select count of **Location** and **Region** where **State** is 'Karnataka', **Region** is 'East', and **Investment** > 300,000"):
    count_location_region_investment = df[(df['State'] == "Karnataka") & 
                                          (df['Region'] == "East") & 
                                          (df['Investment'] > 300000)]['Location'].count()
    st.info(f"## {count_location_region_investment:,}")

# Query 9: Average Investment in Karnataka where Location is not Urban
with st.expander("**QUERY 9:** Select average **Investment** where **State** is 'Karnataka' and **Location** is not 'Urban'"):
    avg_investment_dodoma_not_urban = df[(df['State'] == "Karnataka") & 
                                         (df['Location'] != "Urban")]['Investment'].mean()
    st.info(f"## ₹{avg_investment_dodoma_not_urban:,.2f}")

# Query 10: Sum of Investments in Uttar Pradesh within a date range
with st.expander("**QUERY 10:** Select sum of **Investment** where **State** is Uttar Pradesh and **Expiry** is in the range 2-Jan-21 to 16-Jan-21"):
    sum_investment_date_range = df[(df['Expiry'] >= '2021-01-02') & 
                                   (df['Expiry'] <= '2021-01-16') & 
                                   (df['State'] == 'Uttar Pradesh')]['Investment'].sum()
    st.info(f"## ₹{sum_investment_date_range:,.2f}")