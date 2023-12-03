from app.UI  import UIDesign
from app.api import UrlCall
from app.data import Data
import time
import streamlit as st
import pandas as pd
from datetime import date

from PIL import Image


yellow_taxi_api="http://f39029a1-26c1-4935-a000-96fc84f53841.eastus.azurecontainer.io/score"
green_taxi_api="http://d0ddd7d2-cf15-4649-840d-0ec53a2dffad.eastus.azurecontainer.io/score"
hv_api="http://a6ac78d6-b8a3-4775-a4c4-075213d8b07e.eastus.azurecontainer.io/score"

hv_data=pd.read_csv("./data/fhvhv.csv")
yellow_taxi_data=pd.read_csv("./data/yellow.csv")
green_taxi_data=pd.read_csv("./data/green.csv")


hero=Image.open("./utilis/background/practice.jpg")
# csv_data=pd.read_csv("./data/daily_agg.csv")


# background_image()
st.title("NYC Taxi Ridership Prediction")

st.markdown('''This app uses the services and analysis developed by the ATS Data Analysis team to provide a prediction of the total number of trips on any given day in NYC. The data source is the publically available NYC Trips data. The data is cleaned, parsed, and transformed using Azure Databricks to easily extract the necessary features for ML training. Then the Azure ML Studio is used to train the model on data. We deploy three separate endpoint APIs for the three Taxi types on Azure Services. These can be accessed through a server link. This web app is deployed using Azure Web Application ready to provide trends and predictions based on the necessary inputs.''')
st.image('./utilis/background/purpose2.webp')
st.write("You can try the prediction model below yourself. Adjust parameters according to your need.")
col1, col2, col3 = st.columns(3)
with col1:
  pickup_location = st.selectbox("Pickup Borough", ["Manhattan","Bronx", "Brooklyn", "EWR",  "Queens", "Staten Island" ])
with col2:
  selected_date = st.date_input("Date in the future", date(2023, 1, 1))
year = int(selected_date.year)
month = int(selected_date.month)
day = int(selected_date.day)
selected_day = selected_date.strftime("%A")[0:3]

with col3:
  taxi_type = st.selectbox("Select a taxi", ["Green Taxi", "Yellow Taxi", "High Volume For-Hire Vehicle"])

#  -------------------------------------

data=Data(selected_date=selected_date,selected_day=selected_day,taxi=taxi_type,
          location=pickup_location,yellow_taxi_data=yellow_taxi_data,green_taxi_data=green_taxi_data,hv_data=hv_data)

api_call=UrlCall(headers={'Content-Type':'application/json'})

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            div.embeddedAppMetaInfoBar_container__DxxL1 {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

ui=UIDesign()
# ui.footer()


result=[]

if st.button("Use AI to predict"):
    progress_text = "Prediction in progress. Please wait."

    my_bar = st.progress(0, text=progress_text)
    for percent_complete in range(100):
        time.sleep(0.05)
        my_bar.progress(percent_complete + 1, text=progress_text)


    time.sleep(1)
    date_list=data.date_range()   # date range to be return

    data.previous_values()  # should give reault as the name

    for item in date_list:
      api_parameter=data.api_parameters(single_date_to_predict=item) 
      # api required parameters  
      
      if taxi_type=="Green Taxi":
        api_result=api_call.url_call(url=green_taxi_api,data=api_parameter)
        
      if taxi_type=="High Volume For-Hire Vehicle":
        api_result=api_call.url_call(url=hv_api,data=api_parameter)
        
      if taxi_type=="Yellow Taxi":
        api_result=api_call.url_call(url=yellow_taxi_api,data=api_parameter)

       # give result to url call
      
      api_result=data.clean_result(api_result) # clean the result
      
      result.append(api_result) # result list contain all the predicitve values
      
      days=f"{day}/{month}/{year}" 
      
      listing=[days,pickup_location,taxi_type]
       
    header,subtitle=ui.result_display(result=result[3],description=listing)


    df=data.create_df(results=result) # give dataframe for showing on graphs

    my_bar.empty()
    
    fig,bar_trace=ui.graphs_st(chart_data=df) # for line chart and bar chart
    st.plotly_chart(fig)
    st.plotly_chart(bar_trace) 