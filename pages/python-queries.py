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
df['Expiry'] = pd.to_datetime(df['Expiry'], errors='coerce')
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


with st.expander("**QUERY 11:** select Median of **Investment**  and **Rating** where **State** is Rajasthan, **Location** is Urban and **Investment** is greater than 400,000"):
 query_1 = df[(df['State'] == 'Rajasthan') & (df['Location'] == 'Urban') & (df['Investment'] > 400000)][['Investment', 'Rating']].median()
 st.success("Median of **Investment** and **Rating** where **State** is Rajasthan, **Location** is Urban, and **Investment** is greater than 400,000 USD:")
 st.dataframe(query_1)

# Query 12
with st.expander("**QUERY 12:** Select median of **Investment** and **Rating** where **State** is Rajasthan, **Location** is Urban, **Investment** is greater than 400,000, and **Expiry** is a date range from 2-Jan-21 to 16-Jan-21"):
    # Filter the DataFrame based on the conditions
    filtered_data = df[
        (df['State'] == 'Rajasthan') &
        (df['Location'] == 'Urban') &
        (df['Investment'] > 400000) &
        (df['Expiry'] >= pd.Timestamp('2021-01-02')) &
        (df['Expiry'] <= pd.Timestamp('2021-01-16'))
    ]

    # Calculate the median of 'Investment' and 'Rating'
    median_values = filtered_data[['Investment', 'Rating']].median()

    # Display the results
    st.success("Median of Investment and Rating for the specified conditions:")
    st.dataframe(median_values.to_frame(name="Median Value").reset_index())

st.success("SELECT QUERY RESULTS IN TABULAR")

# Query 12
with st.expander('**QUERY 13:** Select all from **Location** where **Location** ="Tamil Nadu"'):
 st.dataframe(df[df['State'] == "Tamil Nadu"],use_container_width=True)

# Query 14
with st.expander('**QUERY 14:** Select all from **Location** and **Region** where **Location** ="Tamil Nadu" and **Region**="East"'):
 st.dataframe(df[(df['State'] == "Tamil Nadu") & (df['Region'] == "East")],use_container_width=True)

# Query 15
with st.expander('**QUERY 15:** Select all from **Location** and **Region** where **Location** ="Tamil Nadu" and **Region**="East" and **Investment** is greater than 300,000'):
 st.dataframe(df[(df['State'] == "Tamil Nadu") & (df['Region'] == "East") & (df['Investment'] > 300000)],use_container_width=True)

# Query 16
with st.expander('**QUERY 16:** Select all  **investment** where **State**="Tamil Nadu" and **Location** is not "Urban"'):
 st.dataframe(df.loc[(df['State'] == "Tamil Nadu") & (df['Location'] != "Urban"), 'Investment'],use_container_width=True)

# Query 17
with st.expander('**QUERY 17:** select at least 5 most frequent **Investment** where **Expiry** is a date range from 2-jan-21 to 16-jan-21'):
 freq_investment_date_range = df[(df['Expiry'] >= '2021-01-02') & (df['Expiry'] <= '2021-01-16')]['Investment'].value_counts().nlargest(5).reset_index()
 st.dataframe(freq_investment_date_range.rename(columns={'index': 'Investment', 'Investment': 'Count'}))

# Query 18
with st.expander('**QUERY 18:** Select all **investments** where **Expiry** is a date range from 2-Jan-21 to 16-Jan-21 and region is **Tamil Nadu**'):
    filtered_data = df.loc[
        (df['Expiry'] >= pd.Timestamp('2021-01-02')) &
        (df['Expiry'] <= pd.Timestamp('2021-01-16')) &
        (df['State'] == 'Tamil Nadu'),
        ['Investment']
    ]
    st.dataframe(filtered_data, use_container_width=True)

#Query 19
with st.expander("**QUERY 19:** select **State**, **Region**, **Location** and  **BusinessType**  where **Region** is 'East'and **investment** greater than 2219900 and **BusinessType** is not  'Other' and **Construction** is Frame or FireResist and **State** is Karnataka or Tamil Nadu"):
# Applying the specified conditions
 query_result = df[
    (df['Region'] == 'East') &
    (df['Investment'] > 2219900) &
    (df['BusinessType'] != 'Other') &
    (df['Construction'].isin(['Frame', 'Fire Resist'])) &
    (df['State'].isin(['Karnataka', 'Tamil Nadu']))
 ][['State', 'Region', 'Location', 'BusinessType']]
 st.dataframe(query_result,use_container_width=True)