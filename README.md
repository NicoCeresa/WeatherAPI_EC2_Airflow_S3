# Weather API ETL

The script used for this ETL is airflow/dags/weather_dag.py

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
- with the code in `airflow/dags/weather_dag.py` the dag should be all set
- your end result should look like this:

![alt text](https://github.com/NicoCeresa/WeatherAPI_EC2_Airflow_S3/blob/main/Airflow_ETL.png)
