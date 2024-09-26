# https://youtu.be/fgm3BZ3Ubnw?si=rLs7W0J1W2MAm30a
from airflow.models import DAG
from airflow.sensors.filesystem import FileSensor

from datetime import datetime

with DAG(
    "dag_sensor",
    schedule_interval="@daily",
    start_date=datetime(2021, 1, 1),
    catchup=False,
) as dag:
    waiting_for_file = FileSensor(
        task_id="waiting_for_file",
        poke_interval=30,
        timeout=60 * 5,
        mode="reschedule",
        soft_fail=True,
        filepath="/tmp/my_file.txt",
    )
