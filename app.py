import time
import urllib.request
import os
import json
from datetime import date
import holidays
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
url = os.getenv("REST_ENDPOINT")  # REST API endpoint for predictions
api_key = os.getenv("API_KEY")    # API key for authentication

# Configure Streamlit page settings
st.set_page_config(
    page_title="NYC Taxi Demand Forecast",
    page_icon="🚕",
    layout="centered"
)

# Title & about section
st.title("New York Taxi Ridership Prediction")
with st.expander("About this app"):
    st.markdown("""This application is developed by the [ATS AI & Data Analytics team](https://www.atsailab.com/) to estimate the total number of yellow & green taxi trips on any given day in New York city.

**Key components include:**
- **Data Source:** [NYC Taxi Trip Records](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)  
- **ETL:** Data from 2020 to 2024 extracted, transformed and cleaned using **Azure Databricks**  
- **Model Training:** Machine learning model trained using **Azure ML Studio**  
- **Model Deployment:** REST endpoint API hosted on Azure cloud
- **Client Service:** Frontend developed using Streamlit in Python

Project contributors: Abdur Rahman, Ahmed Ali, Usman Sajid & Saad Shakeel.""")
    
st.image("./assets/image.webp", caption="Figure: Understand the Business Problem.")

st.markdown("""
Use machine learning to forecast daily demand for **Yellow** and **Green** taxis across six New York City boroughs.  
Select your desired date, pickup borough, and taxi type, then click **Predict** to view the estimated ridership.
""")

# Get current date for default selection
today = date.today()

# Streamlit UI: Input columns for user selections
col1, col2, col3 = st.columns(3)

with col1:
    # Date input: default is tomorrow
    selected_date = st.date_input(
        label = "📅 Date",
        value = date(today.year, today.month, today.day + 1),
        help = "Select the date you want to predict for. Tomorrow is selected by default."
    )
with col2:
    # Borough selection
    pickup_borough = st.selectbox(
        label = "📍 Pickup Borough", 
        options = ["Manhattan", "Bronx", "Brooklyn", "Queens", "Staten Island","EWR"],
        help = "Select the pickup borough in New York City. 'EWR' refers to Newark Airport.", 
    )
with col3:
    # Taxi type selection
    ride_type = st.selectbox(
        label = "🚖 Ride Type",
        options = ["Yellow Taxi", "Green Taxi"],
        help = "Select the taxi type."
    )

# Helper function: Determine season from month
def get_season(month):
    if 3 <= month <= 5:
        return "Spring"
    elif 6 <= month <=8:
        return "Summer"
    elif 9 <= month <=11:
        return "Autumn"
    else:
        return "Winter"

# Get list of public holidays in New York, USA
nyc_holidays = holidays.country_holidays('US', subdiv='NY')

# Prepare input features for prediction
year = int(selected_date.year)
month = int(selected_date.month)
day = int(selected_date.day)
season = get_season(month)  # Season based on month
public_holiday = 1 if selected_date in nyc_holidays else 0  # Is selected date a public holiday?
day_of_week = selected_date.strftime("%A")[0:3]  # Short day name (e.g., 'Mon')
workday = 1 if day_of_week in ["Mon", "Tue", "Wed", "Thu", "Fri"] else 0  # Is it a workday?

# Construct data dictionary as required by the REST endpoint
data = {
  "input_data": {
    "columns": [
      "PickupBorough",
      "RideType",
      "Year",
      "Month",
      "Day",
      "Season",
      "PublicHoliday",
      "DayOfWeek",
      "Workday"
    ],
    "index": [0],
    "data": [[pickup_borough, ride_type, year, month, day, season, public_holiday, day_of_week, workday]]
}
}

# Encode the data dictionary to JSON for API request
body = str.encode(json.dumps(data))

# Prediction button: triggers API call
if st.button("Predict", type="primary"):
    with st.spinner("Making a prediction...", show_time=True):
        # Check for API key before making request
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint.")

        # Set request headers for REST API
        headers = {'Content-Type':'application/json', 'Accept': 'application/json', 'Authorization':('Bearer '+ api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            # Send request and parse response
            response = urllib.request.urlopen(req)
            result = json.loads(response.read())
            prediction = int(round(result[0]))
            # Display prediction in Streamlit UI
            formatted_date = selected_date.strftime("%d %B %Y")
            st.success(f"On **{formatted_date}**, **{ride_type.lower()}s** are estimated to make **{prediction} trips** from **{pickup_borough}**.")
        except urllib.error.HTTPError as error:
            # Handle HTTP errors and display message
            st.error("The request failed with status code: " + str(error.code))
            # Print error details for debugging
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))