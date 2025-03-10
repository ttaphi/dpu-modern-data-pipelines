from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.utils import timezone

import requests


def _get_weather_data():
    API_KEY = "54b503707289a1074dce85c0be5d9fc9"
    # API_KEY = os.environ.get("WEATHER_API_KEY")
    # API_KEY = Variable.get("weather_api_key")

    payload = {
        "q": "bangkok",
        "appid": API_KEY,
        "units": "metric"
    }
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=payload)
    print(response.url)

    data = response.json()
    print(data)


with DAG(
    "weather_api_dag",
    schedule="@hourly",
    start_date=timezone.datetime(2025, 3, 9),
    tags=["dpu"],
):
    start = EmptyOperator(task_id="start")

    get_weather_data = PythonOperator(
        task_id="get_weather_data",
        python_callable=_get_weather_data,
    )

    end = EmptyOperator(task_id="end")

    start >> get_weather_data >> end