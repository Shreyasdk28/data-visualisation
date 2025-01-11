import pandas as pd
import plotly.express as px
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime
import streamlit as st
import os
from query import view_all_data

# Dummy DataFrame (replace with your actual data)
try:
    df = view_all_data()  # Ensure view_all_data returns a DataFrame
except Exception as e:
    st.error(f"Error fetching data: {e}")
    st.stop()

# Directory to store the images for the report
output_folder = "C:/Users/vishe/OneDrive/Desktop/data-visualisation/data-visualisation/Reports"  # Update with your own path  # Update with your own path

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Generate Report (with charts and textual info)
def generate_pdf(df):
    # Create a PDF file
    pdf_file = BytesIO()
    c = canvas.Canvas(pdf_file, pagesize=letter)
    width, height = letter

    # Add a Title Page
    c.setFont("Helvetica-Bold", 20)
    c.drawString(200, 750, "Investment Report")
    c.setFont("Helvetica", 12)
    c.drawString(200, 730, f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    c.showPage()

    # Executive Summary
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, 750, "Executive Summary")
    c.setFont("Helvetica", 12)
    c.drawString(30, 730, "This report provides key insights based on the selected data filters. Below are the key metrics:")

    # Add a few textual metrics
    total_investment = df['Investment'].sum()
    avg_investment = df['Investment'].mean()
    c.drawString(30, 710, f"Total Investment: ₹{total_investment}")
    c.drawString(30, 690, f"Average Investment: ₹{avg_investment}")
    c.showPage()

    # Investment by Region (Bar Chart)
    region_investment = df.groupby("Region")["Investment"].sum().reset_index()
    fig_region = px.bar(region_investment, x="Region", y="Investment", title="Investment by Region")
    region_image_path = os.path.join(output_folder, "region_investment.png")
    fig_region.write_image(region_image_path)

    c.drawString(30, 750, "Investment by Region")
    c.drawImage(region_image_path, 30, 500, width=500, height=250)
    c.showPage()

    # Investment by Business Type (Pie Chart)
    business_investment = df.groupby("BusinessType")["Investment"].sum().reset_index()
    fig_business = px.pie(business_investment, values="Investment", names="BusinessType", title="Investment by Business Type")
    business_image_path = os.path.join(output_folder, "business_investment.png")
    fig_business.write_image(business_image_path)

    c.drawString(30, 750, "Investment by Business Type")
    c.drawImage(business_image_path, 30, 500, width=500, height=250)
    c.showPage()

    # Ratings Overview (Text + Bar Chart)
    avg_rating = df["Rating"].mean()
    c.drawString(30, 750, f"Average Rating: {avg_rating}")
    c.drawString(30, 730, "Ratings Distribution")
    fig_rating = px.bar(df, x="BusinessType", y="Rating", title="Ratings by Business Type")
    ratings_image_path = os.path.join(output_folder, "ratings_distribution.png")
    fig_rating.write_image(ratings_image_path)
    c.drawImage(ratings_image_path, 30, 500, width=500, height=250)
    c.showPage()

    # Concluding Remarks
    c.setFont("Helvetica-Bold", 16)
    c.drawString(30, 750, "Concluding Remarks")
    c.setFont("Helvetica", 12)
    c.drawString(30, 730, "Based on the data analysis, the following insights can be drawn:")
    c.drawString(30, 710, "1. The North region holds the largest share of investment.")
    c.drawString(30, 690, "2. Corporate business types have the highest total investment.")
    c.drawString(30, 670, "3. The average rating across all policies is above 4.0.")

    c.showPage()

    # Save PDF to the BytesIO buffer
    c.save()

    # Provide message after download
    print("PDF Report Generated Successfully!")
    pdf_file.seek(0)  # Move to the start of the BytesIO buffer for download
    return pdf_file

# Function to display download button in Streamlit
def show_download_button(pdf_file):
    st.download_button(
        label="Download Report",
        data=pdf_file,
        file_name="investment_report.pdf",
        mime="application/pdf"
    )

# Generate PDF and provide download button in Streamlit
pdf_file = generate_pdf(df)
show_download_button(pdf_file)

