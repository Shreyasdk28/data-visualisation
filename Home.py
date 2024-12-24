import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
theme_plotly = None 
# from query import view_all_data
import plotly.graph_objs as go

st.set_page_config(page_title="Dashboard",page_icon="🌍",layout="wide")
st.header("ANALYTICAL PROCESSING, KPI, TRENDS & PREDICTIONS")
with open('style.css')as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)
# # Database connection
# try:
#     conn = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="",
#         database="mydb"
#     )
#     # st.success("Database connected!")
# except mysql.connector.Error as e:
#     st.error(f"Database connection failed: {e}")
#     st.stop()  # Stop execution if the database connection fails

# # Fetch data function
# def view_all_data():
#     try:
#         cursor = conn.cursor()
#         cursor.execute("SELECT * FROM insurance ORDER BY id ASC")
#         result = cursor.fetchall()
#         return result
#     except mysql.connector.Error as e:
#         st.error(f"Failed to fetch data: {e}")
#         return []

# Fetch and display data
# with st.spinner("Fetching data from the database..."):
#     result =pd.read_csv("data/data.csv")
#     if result:
#         df = pd.DataFrame(result, columns=[
#             "Policy", "Expiry", "Location", "State", "Region",
#             "Investment", "Construction", "BusinessType",
#             "Earthquake", "Flood", "Rating"
#         ])
#         #st.dataframe(df)
#     else:
#         st.warning("No data found!")

# # Sidebar filters
# if not result:
#     st.stop()  # Stop further execution if no data is retrieved
df=pd.read_csv("data/data.csv")
st.sidebar.image("data/logo1.png", caption="Online Analytics")
st.sidebar.header("Please filter the data")
region = st.sidebar.multiselect(
"Select Region", options=df["Region"].unique(), default=df["Region"].unique()
)

location = st.sidebar.multiselect(
    "Select Location", options=df["Location"].unique(), default=df["Location"].unique()
)

construction = st.sidebar.multiselect(
    "Select Construction", options=df["Construction"].unique(), default=df["Construction"].unique()
)

df_selection=df.query(
    "Region == @region & Location == @location & Construction == @construction"
)

#st.dataframe(df_selection)

def Home():
    with st.expander("VIEW EXCEL DATASET"):
        showData=st.multiselect('Filter: ',df_selection.columns,default=["Policy","Expiry","Location","State","Region","Investment","Construction","BusinessType","Earthquake","Flood","Rating"])
        st.dataframe(df_selection[showData],use_container_width=True)
    #compute top analytics 
    # Total investment (no need for empty check as sum always returns a number)
    # Total Investment
    total_investment = df_selection["Investment"].sum() 
    total_investment = int(total_investment)

    if pd.isna(total_investment):
        total_investment = 0
    # Mode of the 'Investment' column
    mode_series = df_selection['Investment'].mode()

    investment_mode = float(mode_series.iloc[0]) if not mode_series.empty else 0

    # Mean of the 'Investment' column
    # Mean of the 'Investment' column
    investment_mean = df_selection['Investment'].mean() 


# Median of the 'Investment' column
    investment_median = df_selection['Investment'].median()

# Sum of the 'Rating' column
    rating = df_selection['Rating'].sum() 

# Handle potential NaN values
    if pd.isna(investment_mean):
        investment_mean = 0
    if pd.isna(investment_median):
        investment_median = 0
    if pd.isna(rating):
        rating = 0

    total1,total2,total3,total4,total5=st.columns(5,gap='large')
    with total1:
        st.info('Sum Investment',icon="💰")
        st.metric(label='sum',value=f"₹{numerize(total_investment)}",help=f""" Total investment: {total_investment}""")
    with total2:
        st.info('Most Investment',icon="💰")
        st.metric(label='mode',value=f"₹{numerize(investment_mode)}",help=f""" Total investment: {investment_mode}""")
    with total3:
        st.info('Average',icon="💰")
        st.metric(label='average',value=f"₹{numerize(investment_mean)}",help=f""" Total investment: {investment_mean}""")
    with total4:
        st.info('Central Earnings',icon="💰")
        st.metric(label='median',value=f"₹{numerize(investment_median)}",help=f""" Total investment: {investment_median}""")
    with total5:
        st.info('Ratings',icon="💰")
        st.metric(label='Rating',value=numerize(rating),help=f""" Total Rating: {rating }""")
    style_metric_cards(background_color="#FFFFFF",border_left_color="#686664",border_color="#000000",box_shadow="#F71938")
    
    with st.expander("DISTRIBUTIONS BY FREQUENCY"):
      df.hist(figsize=(16,8),color='#898784', zorder=2, rwidth=0.9,legend = ['Investment']);
      st.pyplot()

# Home()

#graphs

def graphs():
    total_investment = int(df_selection["Investment"].sum())
    average_rating=int(round(df_selection["Rating"].mean(),2))
    #simple bar graph
    investment_by_business_type = (df_selection.groupby("BusinessType").count()[["Investment"]].sort_values(by="Investment"))
    fig_investment=px.bar(
        investment_by_business_type,
        x="Investment",
        y=investment_by_business_type.index,
        orientation="h",
        title="<b>Investment by Business Type</b>",
        color_discrete_sequence=["#0083B8"]*len(investment_by_business_type),
        template="plotly_white",
        )
    fig_investment.update_layout(
     plot_bgcolor="rgba(0,0,0,0)",
     font=dict(color="black"),
     yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color  
     paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
     xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
     )
    

    #simple line grpah
    investment_state= df_selection.groupby("State").count()[["Investment"]]
    fig_state=px.line(
        investment_state,
        x=investment_state.index,
        y="Investment",
        orientation="v",
        title="<b>Investment by State</b>",
        color_discrete_sequence=["#0083b8"]*len(investment_state),
        template="plotly_white",
        )
    fig_state.update_layout(
        xaxis=(dict(tickmode="linear")),
        plot_bgcolor='rgba(0,0,0,0)',
        yaxis=(dict(showgrid=False)))
    left,right,center=st.columns(3)
    left.plotly_chart(fig_state,use_container_width=True)
    right.plotly_chart(fig_investment,use_container_width=True)
    with center:
      #pie chart
      fig = px.pie(df_selection, values='Rating', names='State', title='RATINGS BY REGIONS')
      fig.update_layout(legend_title="Regions", legend_y=0.9)
      fig.update_traces(textinfo='percent+label', textposition='inside')
      st.plotly_chart(fig, use_container_width=True, theme=theme_plotly)

def progressbar():
    st.markdown("""<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",unsafe_allow_html=True,)
    target=3000000000
    current=df_selection["Investment"].sum()
    percent = round((current/target)*100)
    mybar = st.progress(0)
    if percent>100:
        st.subheader("Target Achieved")
    else:
        st.write("you hvae ", percent,"% ", "of ", numerize(target), "$")   
        for percent_complete in range(percent):
            time.sleep(0.08)
            mybar.progress(percent_complete+1, text=f"{percent_complete+1}%") 
    
# progressbar()
import streamlit as st
from streamlit_option_menu import option_menu

def sidebar(): 
    with st.sidebar:
        selected = option_menu(
            menu_title="Main Menu",
            options=["Home", "Progress"],
            icons=["house", "eye"],
            menu_icon="cast",
            default_index=0
        )
    
    if selected == "Home":
        st.subheader(f"Page: {selected}")
        Home()
        graphs()
    
    if selected == "Progress":
        st.subheader(f"Page: {selected}")
        progressbar()
        graphs()

sidebar()

st.subheader('PICK FEATURES TO EXPLORE DISTRIBUTIONS TRENDS BY QUARTILES',)
feature_x = st.selectbox('Select feature for x Qualitative data', df_selection.select_dtypes("object").columns)
feature_y = st.selectbox('Select feature for y Quantitative Data', df_selection.select_dtypes("number").columns)
fig2 = go.Figure(
    data=[go.Box(x=df['BusinessType'], y=df[feature_y])],
    layout=go.Layout(
        title=go.layout.Title(text="BUSINESS TYPE BY QUARTILES OF INVESTMENT"),
        plot_bgcolor='rgba(0, 0, 0, 0)',  # Set plot background color to transparent
        paper_bgcolor='rgba(0, 0, 0, 0)',  # Set paper background color to transparent
        xaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show x-axis grid and set its color
        yaxis=dict(showgrid=True, gridcolor='#cecdcd'),  # Show y-axis grid and set its color
        font=dict(color='#cecdcd'),  # Set text color to black
    )
)

#display it
st.plotly_chart(fig2, use_container_width=True)
#theme

hide_st_style=""" 

<style>
    #MainMenu {visibility:hidden;}
    footer {visibility:hidden;}
    header {visibility:hidden;}
</style>
"""

