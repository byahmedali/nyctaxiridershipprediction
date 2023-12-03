import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import base64
import pandas as pd
import streamlit as st
from PIL import Image

#  bold color

image=Image.open("./utilis/background/practice.jpg")
class UIDesign:
    def __init__(self) -> None:
        pass

    def back_ground(self,image):
         # Resize the image
        resized_img = image.resize((100, 100))

        # Convert the resized image to base64
        encoded_image = base64.b64encode(resized_img.tobytes()).decode()

        # Embed the HTML code in Streamlit app
        markdown=f"""
            <style>
                [data-testid="stAppViewContainer"] {{
                    background: url(data:image/{resized_img};base64,{base64.b64encode(open(resized_img, "rb").read()).decode()});
                    background-size: cover;
                    background-repeat: no-repeat;
                }}
                [data-testid="stHeader"] {{
                    visibility: hidden;
                }}
            </style>
            """
        return markdown

    def hero_img(self, text, subtitle,image2):
        
        hero_img_mark = f"""
            <style>
                body {{
                    margin: 0;
                    padding: 0;
                    font-family: Arial, sans-serif;
                }} 
                .hero-container {{
                    position: relative;
                    width: 100%;
                    height: 500px; /* Adjust the height as needed */
                    overflow: hidden;
                    text-align: center;
                    color: #fff; /* Set text color */
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }} 
                .hero-img {{
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    object-fit: cover;
                    object-position: center;
                }} 
                .hero-text {{
                    z-index: 1;
                    max-width: 800px;
                    margin: 0 auto;
                    padding: 20px;
                }} 

                .hero-text h1 {{
                    font-size: 36px; /* Adjust the font size as needed */
                    margin-bottom: 20px;
                }}

                .hero-text p {{
                    font-size: 18px; /* Adjust the font size as needed */
                    margin-bottom: 20px;
                }} 
            </style>
            <div class="hero-container">
                <img class="hero-img" src=https://media.wired.com/photos/595485ddce3e5e760d52d542/master/w_1600,c_limit/GettyImages-182859572.jpg
                 alt="Hero Image">
                <div class="hero-text">
                    <h1>{text}</h1>
                    <p>{subtitle}</p>
                </div>
            </div>
        """
        st.markdown(hero_img_mark, unsafe_allow_html=True)

    def result_display(self,result,description):
        header_markdown = f"""
            
            <div class="hero-text234">
            <strong><h>{result}</h></strong>
            </div>
        """
        subtitle_markdown = f"""
           
        
            <style>
                mark {{
                    background-color: white;
                    color: black;
                }}
                #popup {{
                text-align: center;
                font-size: 25px; /* Adjust the font size as needed */
                margin-top: 10px;
                margin-left:%;
                position: relative;
                margin-top:150px;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                width: 750px;
                height: 250px;
                box-shadow: 0 0 50px 1px rgba(0, 0, 0, 0.5);
                padding-top: 30px
                }}
                .hero-text234 h{{
                    font-size: 70px; /* Adjust the font size as needed */
                    
                    
                }}
            </style>

            <div id="popup">
                <div style="margin-top: 25px;">
                    <p style="font-size: 20px;">
                        Total Number of Trips Expected on
                        <mark ><strong><span style="color: black;">{description[0]}</span></strong></mark>
                        from
                        <mark ><strong><span style="color: black;">{description[1]}</span></strong></mark>
                        for
                        <mark ><strong><span style="color: black;">{description[2]}</span></strong></mark>
                    </p>
                </div>
                <div class="hero-text234">
                    <strong>
                        <h>{result}</h>
                    </strong>
                </div>
            </div>


        """
        # st.markdown(header_markdown, unsafe_allow_html=True)
        st.markdown(subtitle_markdown, unsafe_allow_html=True)
        
        return header_markdown,subtitle_markdown
    
    def footer(self):
        # Custom footer
        footer_html = """
            <style>
            #MainMenu{
                visivility:hidden;
            }
            footer{
            visibility:visible;
            }
            footer:after{
                content: By Usman Sajid  @ 2023: ATS;
                display:block;
                position:relative;
                color:tomato;
                padding:5px;
                top:3px;
            }
            </style>
           
        """
        # Display the footer
        st.markdown(footer_html, unsafe_allow_html=True)

        
        
       
    def graphs_st(self,chart_data):
        """Showing graphs of dates and their respective results."""
        
        # Print the lengths of 'Date' and each y-value column
        print(chart_data.columns)

        fig = px.line(chart_data, x='Date', y=['Predicted_Values', '2020', '2021', '2022'], markers=True, title="Graph of Dates and Results")
        chart_data['Color'] = chart_data['Percentage'].apply(lambda x: 'Positive Change' if x < 0 else "Negative Change")

    # Plot the bar chart with color based on the "Color" column
        bar_trace = px.bar(
            chart_data,
            x="Date",
            y='Percentage',
            title="NYC Taxi-Ride count percentage",
            color='Color',
        )
        return fig,bar_trace
    # 2022, perdict
# percentage change =predict-2022/2022
# expected percent chage fom 2022
#  

        

            
            