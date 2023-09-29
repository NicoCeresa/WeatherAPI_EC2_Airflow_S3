import json
import pandas as pd
from airflow import DAG
from key_secret_token import aws_credentials
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator


def kelvin_to_fahrenheit(temp_in_kelvin):
        return (temp_in_kelvin - 273.15) * (9/5) + 32

def transform_load_data(task_instance):
        data = task_instance.xcom_pull(task_ids='extract_weather_data')
        city = data['name']
        weather_description = data['weather'][0]['description']
        temp_fahrenheit = kelvin_to_fahrenheit(data['main']['temp'])
        feels_like_fahrenheit = kelvin_to_fahrenheit(data['main']['feels_like'])
        min_temp_fahrenheit = kelvin_to_fahrenheit(data['main']['temp_min'])
        max_temp_fahrenheit = kelvin_to_fahrenheit(data['main']['temp_max'])
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
        sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
        sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])

        transformed_data = {"City": city,
                        "Description": weather_description,
                        "Temperature (F)": temp_fahrenheit,
                        "Feels Like (F)": feels_like_fahrenheit,
                        "Minimun Temp (F)":min_temp_fahrenheit,
                        "Maximum Temp (F)": max_temp_fahrenheit,
                        "Pressure": pressure,
                        "Humidty": humidity,
                        "Wind Speed": wind_speed,
                        "Time of Record": time_of_record,
                        "Sunrise (Local Time)":sunrise_time,
                        "Sunset (Local Time)": sunset_time                        
                        }
        
        df_data = pd.DataFrame([transformed_data])
        now = datetime.now()
        dt_str = now.strftime("%d%m%Y%H%M%S")
        dt_str = 'current_weather_in_oakland' + dt_str
        df_data.to_csv(f"s3://weather-api-airflow-bucket-nico/{dt_str}.csv", index=False, storage_options=aws_credentials)


default_args = {
    'owner':'airflow',
    'depends_on_past':False,
    'start_date':datetime(2023, 1, 8),
    'email':['ceresanico@gmail.com'],
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':2,
    'retry_delay':timedelta(minutes=2)
}


with DAG('weather_dag_yt',
         default_args=default_args,
         schedule_interval= '@daily',
         catchup=False) as dag:
        
        is_weather_api_ready = HttpSensor(
                task_id='is_weather_api_ready',
                http_conn_id='weathermap_api',
                endpoint='/data/2.5/weather?q=Oakland&appid=ce935208616679fd075d01af9bd113c0'
        )

        extract_weather_data = SimpleHttpOperator(
                task_id='extract_weather_data',
                http_conn_id='weathermap_api',
                endpoint='/data/2.5/weather?q=Oakland&appid=ce935208616679fd075d01af9bd113c0',
                method='GET',
                response_filter= lambda r: json.loads(r.text),
                log_response=True
        )
        

        transform_load_weather_data = PythonOperator(
                task_id='transform_load_weather_data',
                python_callable=transform_load_data
        )

        is_weather_api_ready >> extract_weather_data >> transform_load_weather_data