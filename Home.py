import streamlit as st
# Ensure this is at the very top of your script
if "page_config_set" not in st.session_state:
    st.set_page_config(page_title="Dashboard", page_icon="🌍", layout="wide")
    st.session_state.page_config_set = True  # Prevent multiple calls to set_page_config

import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from streamlit_option_menu import option_menu
from numerize.numerize import numerize
import time
from streamlit_extras.metric_cards import style_metric_cards
from query import view_all_data  # Ensure this function is correctly implemented
import plotly.graph_objs as go 

# Page header
st.header("ANALYTICAL PROCESSING, KPI, TRENDS & PREDICTIONS")

# Load external CSS
with open('style.css') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Fetch data
try:
    df = view_all_data()  # Ensure view_all_data returns a DataFrame
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# Sidebar setup
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
df_selection = df.query(
    "Region == @region & Location == @location & Construction == @construction"
)

# Function to display the home page
def Home():
    # Data preview
    with st.expander("VIEW EXCEL DATASET"):
        show_data = st.multiselect(
            "Filter: ", df_selection.columns,
            default=[
                "Policy", "Expiry", "Location", "State", "Region",
                "Investment", "Construction", "BusinessType", "Earthquake", "Flood", "Rating"
            ]
        )
        st.dataframe(df_selection[show_data], use_container_width=True)

    # Calculate analytics
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



    # Distribution chart
    with st.expander("DISTRIBUTIONS BY FREQUENCY"):
        # Create a figure and axis object
        fig, ax = plt.subplots(figsize=(16, 8))  # Specify the size of the plot
        
        # Plot the histogram
        df.hist(ax=ax, color='#898784', zorder=2, rwidth=0.9, legend=['Investment'])
        
        # Use st.pyplot with the figure and axis
        st.pyplot(fig)  # Pass the created figure

# Function to display graphs
def graphs():
    # Grouping for bar graph
    investment_by_business_type = df_selection.groupby("BusinessType")["Investment"].sum().reset_index()
    fig_investment = px.bar(
        investment_by_business_type,
        x="Investment",
        y="BusinessType",
        orientation="h",
        title="<b>Investment by Business Type</b>",
        color_discrete_sequence=["#0083B8"] * len(investment_by_business_type),
        template="plotly_white"
    )
    fig_investment.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="black"),
        yaxis=dict(showgrid=True, gridcolor="#cecdcd"),
        paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(showgrid=True, gridcolor="#cecdcd"),
    )

    # Line graph
    investment_state = df_selection.groupby("State")["Investment"].sum().reset_index()
    fig_state = px.line(
        investment_state,
        x="State",
        y="Investment",
        title="<b>Investment by State</b>",
        color_discrete_sequence=["#0083b8"] * len(investment_state),
        template="plotly_white"
    )
    fig_state.update_layout(
        xaxis=dict(tickmode="linear"),
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(showgrid=False),
    )

    # Pie chart
    fig_pie = px.pie(df_selection, values="Rating", names="State", title="RATINGS BY REGIONS")
    fig_pie.update_layout(legend_title="Regions", legend_y=0.9)
    fig_pie.update_traces(textinfo="percent+label", textposition="inside")

    # Display graphs
    left, right, center = st.columns(3)
    left.plotly_chart(fig_state, use_container_width=True)
    right.plotly_chart(fig_investment, use_container_width=True)
    center.plotly_chart(fig_pie, use_container_width=True)

# Function for the progress bar
def progressbar():
    st.markdown(
        """<style>.stProgress > div > div > div > div { background-image: linear-gradient(to right, #99ff99 , #FFFF00)}</style>""",
        unsafe_allow_html=True,
    )
    target = 3000000000
    current = df_selection["Investment"].sum()
    percent = round((current / target) * 100)
    mybar = st.progress(0)

    if percent > 100:
        st.subheader("Target Achieved")
    else:
        st.write(f"You have achieved {percent}% of ₹{numerize(target)}")
        for percent_complete in range(percent):
            time.sleep(0.08)
            mybar.progress(percent_complete + 1, text=f"{percent_complete + 1}%")

# Sidebar navigation
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
        Home()
        graphs()
    elif selected == "Progress":
        progressbar()
        graphs()

sidebar()

# Additional visualizations
st.subheader("PICK FEATURES TO EXPLORE DISTRIBUTIONS & TRENDS BY QUARTILES")
feature_x = st.selectbox("Select feature for X (Qualitative)", df_selection.select_dtypes("object").columns)
feature_y = st.selectbox("Select feature for Y (Quantitative)", df_selection.select_dtypes("number").columns)

fig_quartiles = go.Figure(
    data=[go.Box(x=df_selection[feature_x], y=df_selection[feature_y])],
    layout=go.Layout(
        title="Business Type by Quartiles of Investment",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        xaxis=dict(showgrid=True, gridcolor="#cecdcd"),
        yaxis=dict(showgrid=True, gridcolor="#cecdcd"),
        font=dict(color="#cecdcd"),
    )
)
st.plotly_chart(fig_quartiles, use_container_width=True)

# Hide default Streamlit UI
st.markdown(
    """
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)
