"""A working example from the video below.

https://www.youtube.com/watch?v=IH1-0hwFZRQ&list=PL79i7SgJCJ9hf7JgG3S-3lOpsk2QCpWkD&index=4
"""

from datetime import datetime
from random import randint

from airflow import DAG
from airflow.decorators import task
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator


with DAG(
    "my_dag",
    start_date=datetime(2021, 1, 1),
    schedule="@daily",
    description="Training ML Models.",
    tags=["data_engineering", "Mark"],
    catchup=False,
):

    @task
    def training_model():
        return randint(1, 10)

    @task.branch
    def choose_best_model(accuracies):
        best_accuracy = max(accuracies)
        if best_accuracy > 8:
            return "accurate"
        return "inaccurate"

    accurate = BashOperator(task_id="accurate", bash_command="echo 'accurate'")
    inaccurate = BashOperator(task_id="inaccurate", bash_command="echo 'inaccurate'")

    choose_best_model(training_model())
