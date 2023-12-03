import pandas as pd

class Data:
    def __init__(self,selected_date,taxi,location,selected_day,yellow_taxi_data,green_taxi_data,hv_data,**kwargs) -> None:
        
        self.selected_date=selected_date
        self.selected_taxi="Green Taxi"
        self.selected_day=selected_day
        self.location=location
        
        #  data of csv
        self.y_taxi=yellow_taxi_data
        self.g_taxi=green_taxi_data
        self.hv=hv_data

        self.dicti=kwargs
        self.dates_list=[]
        self.previous_year_ride_counts={}


    def date_range(self):
        dates_list=[item.strftime("%Y/%m/%d") for item in  pd.date_range(pd.Timestamp(self.selected_date)-pd.offsets.Day(3),freq='D',periods=5)]
        future_dates=[item for item in pd.date_range(start=pd.Timestamp(self.selected_date)+pd.offsets.Day(2),freq='D',periods=2)]
        for item in future_dates:
            dates_list.append(item.strftime('%Y/%m/%d'))
        self.dates_list=dates_list
        return dates_list

    def previous_values(self)->dict:
        """if you want to show graphs of dates that are present in df"""
        previ=["2020","2021","2022"]
        for previous_year in previ:
            single_year_data=[]
            for single_date in self.dates_list:
                month1 = str(single_date[5:7])
                day1=str(single_date[8:])
                # print(single_date)
                x=previous_year+"-"+month1+"-"+day1
                dataframe1,condition_mask=None,None
                conditions={
                    "PickupBorough":self.location,
                    "RideType":self.selected_taxi,
                    "Date":x
                }
                
                
                # print(self.y_taxi.Date[f"{previous_year}-{month1}-{day1}"])
                print(f"location: {self.location},ridetype: {self.selected_taxi},date: ")
#  1 cond
                if self.selected_taxi=="Green Taxi":
                    dataframe1=self.g_taxi
                    condition_mask = (
                        (dataframe1['PickupBorough'] == conditions['PickupBorough']) &
                        (dataframe1['RideType'] == conditions['RideType']) &
                        (dataframe1['Date'] == conditions['Date'])
                    )
#  2 cond

                elif self.selected_taxi=="Yellow Taxi":
                    dataframe1=self.y_taxi
                    condition_mask = (
                        (dataframe1['PickupBorough'] == conditions['PickupBorough']) &
                        (dataframe1['RideType'] == conditions['RideType']) &
                        (dataframe1['Date'] == conditions['Date'])
                    )

                else:
                    dataframe1=self.hv
                    conditions["RideType"]="FHVHV Taxi"
                    condition_mask = (
                        (dataframe1['PickupBorough'] == conditions['PickupBorough']) &
                        (dataframe1['RideType'] == conditions['RideType']) &
                        (dataframe1['Date'] == conditions['Date'])
                    )
                
                RC_for_previous_year = dataframe1.RideCount[condition_mask]
                print(RC_for_previous_year.iloc[:0])
                single_year_data.append(int(RC_for_previous_year))
            self.previous_year_ride_counts[previous_year]=single_year_data

    def workday_con(self)->bool:
        """conditions for checking season and workday"""
        if self.selected_day  in ["Mon","Tue","Wed","Thu","Fri"]:
            workday=1
            return workday
        else:
            workday=0
            return workday
        
    def selected_season_con(self,month)->str:
        if month in [12, 1, 2]:
            season="Winter"
            return season
        elif month in [3, 4, 5]:
            season="Spring"
            return season
        elif month in [6, 7, 8]:
            season="Summer"
            return season
        elif month in [9, 10, 11]:
            season="Autumn"
            return season
        
    def checking_results(result:int)->int:
        if result < 0:
            result=0
        elif result >= 0:
            pass
        return result
    
    def api_parameters(self,single_date_to_predict)->dict:
        year1 = int(single_date_to_predict[:4])
        month1 = int(single_date_to_predict[5:7])
        day1=int(single_date_to_predict[9:])
        workday=self.workday_con()
        season=self.selected_season_con(month=self.selected_date.month)
        data =  {
        "Inputs": {
            "data": [
            {
                "PickupBorough": self.location, 
                "Year": year1, 
                "Month": month1,
                "Day": day1, 
                "Season": season, 
                "DayOfWeek": self.selected_day, 
                "Workday": workday
            }
            ]
        },
        "GlobalParameters": 1.0
        }
        return data
    
    def clean_result(self,api_result)->int:
        if api_result < 0:
            api_result=0
        elif api_result >= 0:
            pass
        return api_result
    
    def percentage(self,year_2022_values,predicted_values):
        percen_list = percen_list = [round(((int(predict_value) - int(values_2022)) / int(values_2022)) * 100, 3) if int(values_2022) != 0  else 1  for values_2022, predict_value in zip(year_2022_values, predicted_values)]
        return percen_list
    
    def create_df(self,results):
        data_2021=self.previous_year_ride_counts["2021"]
        data_2022=self.previous_year_ride_counts["2022"]
        data_2020=self.previous_year_ride_counts["2020"]
        
        # Convert dates to strings
        percentage_values=self.percentage(year_2022_values=data_2022,predicted_values=results)
        if len(self.dates_list) != len(results):
            return "Error: The 'dates' and 'results' lists must have the same length."
        else:
            try:
                chart_data = pd.DataFrame({
                    "Date": self.dates_list,
                    "Predicted_Values": results,
                    "2021": data_2021,
                    "2022": data_2022,
                    "2020":data_2020,
                    "Percentage":percentage_values
                })
            except:
                print("error")

        return chart_data


  