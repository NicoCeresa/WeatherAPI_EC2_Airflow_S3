# Weather API ETL

**Note:** These are just the very base files for this project and do not include any secrets, tokens, or anything of the like

## Overview
- In this project I used the openweathermap.org API to pull data on the climate of a city such as weather description, temp, feels like temp, daily minimum temp, daily maximum temp, pressure, humidity, wind speed, time of record, sunrise and sunset time
- I did this for the city of Oakland but this can be easily changed to any city you would like

## Technologies used
- AWS EC2
- Apache-Airflow
- AWS S3

## How Was This Done?

### Step 1: Create an EC2 instance
- An EC2 (Amazon Elastic Compute Cloud) instance is simply a virtual server in Amazon Web Services terminology.
- create an instance on an Ubuntu platform
- make the instance type t2.small
- make sure it is public, not private

### Step 2: SSH into your virtual Ubuntu machine
- install dependencies:
  - sudo apt update
  - sudo apt install python3-pip
  - sudo apt install python3.10-venv
  - python3 -m venv airflow_venv
  - sudo pip install pandas
  - sudo pip install s3fs
  - sudo pip install apache-airflow
 
### Step 3: Run Airflow
- use the command:  `airflow standalone` to launch apache-airflow
- use the given credentials to sign in

### Step 4: Start DAG
- with the code in `weather_dag.py` the dag should be all set
- your end result should look like this:

![alt text](https://github.com/NicoCeresa/WeatherAPI_EC2_Airflow_S3/blob/main/Airflow_ETL.png)
