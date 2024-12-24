import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_extras.metric_cards import style_metric_cards

st.set_page_config(page_title="Dashboard", page_icon="📈", layout="wide")  
st.subheader("PYTHON QUERY OPERATIONS | FETCH DATA FROM DATASET BY ADVANCED QUERY")

theme_plotly = None 

#sidebar
st.sidebar.image("data/logo1.png")

# load Style css
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
    
# Load the Excel file into a DataFrame
file_path = 'python_query.xlsx'  
df = pd.read_excel(file_path)

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

# Query 5
with st.expander("**QUERY 5:** select minimal **Investment** and minimal **Rating** where **State** is Mwanza and Expiry date is range from 2-jan-21 to 16-jan-21"):
 query_5 = df[(df['State'] == 'Mwanza') & (df['Expiry'] >= '2021-01-02') & (df['Expiry'] <= '2021-01-16')][['Investment', 'Rating']].agg('min')
 st.success("Minimum **Investment** and **Rating** where **State** is **Mwanza** and date is in the specified range:")
 st.dataframe(query_5)

# Query 6
with st.expander("**QUERY 6:** select count **Location** where **Location** ='Dodoma'"):
 count_location = df[df['State'] == "Dodoma"]['Location'].count()
 st.info(f"## {count_location}")

# Query 7
with st.expander("**QUERY 7:**  select count  **Location** and **Region** where **Location** ='Dodoma' and **Region**='East'"):
 count_location_region = df[(df['State'] == "Dodoma") & (df['Region'] == "East")]['Location'].count()
 st.info(f"## {count_location_region:,.3f}")

# Query 8
with st.expander("**QUERY 8:** select count **Location** and **Region** where **Location** ='Dodoma' and **Region**='East' and **Investment** is greater than 300000"):
 count_location_region_investment = df[(df['State'] == "Dodoma") & (df['Region'] == "East") & (df['Investment'] > 300000)]['Location'].count()
 st.info(f"## {count_location_region_investment:,.3f}")

# Query 9
with st.expander("**QUERY 9:** select average mean of **investment** where **State**='Dodoma' and **Location** is not  'Urban'"):
 avg_investment_dodoma_not_urban = df[(df['State'] == "Dodoma") & (df['Location'] != "Urban")]['Investment'].mean()
 st.info(f"## {avg_investment_dodoma_not_urban:,.3f} ")


# Query 10- Sum of investments in the date range at Dodoma
with st.expander("**QUERY 10:** select summation of **investment** where **Expiry** is a date range from 2-jan-21 to 16-jan-21 and region is Dodoma"):
 sum_investment_date_range_dodoma = df[(df['Expiry'] >= '2021-01-02') & (df['Expiry'] <= '2021-01-16') & (df['State'] == 'Dodoma')]['Investment'].sum()
 st.info(f"## {sum_investment_date_range_dodoma:,.3f}")