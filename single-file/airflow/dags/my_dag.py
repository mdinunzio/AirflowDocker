"""A working example from the video below.

https://www.youtube.com/watch?v=IH1-0hwFZRQ&list=PL79i7SgJCJ9hf7JgG3S-3lOpsk2QCpWkD&index=4
"""

from datetime import datetime
from random import randint

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator


def _choose_best_model(ti):
    accuracies = ti.xcom_pull(
        task_ids=[
            "training_model_A",
            "training_model_B",
            "training_model_C",
        ]
    )
    best_accuracy = max(accuracies)
    if best_accuracy > 8:
        return "accurate"
    return "inaccurate"


def _training_model():
    return randint(1, 10)


with DAG(
    "my_dag",
    start_date=datetime(2021, 1, 1),
    schedule="@daily",
    description="Training ML Models.",
    tags=["data_engineering", "Mark"],
    catchup=False,
) as dag:
    training_model_A = PythonOperator(
        task_id="training_model_A", python_callable=_training_model
    )

    training_model_B = PythonOperator(
        task_id="training_model_B", python_callable=_training_model
    )

    training_model_C = PythonOperator(
        task_id="training_model_C", python_callable=_training_model
    )

    choose_best_model = BranchPythonOperator(
        task_id="choose_best_model", python_callable=_choose_best_model
    )

    accurate = BashOperator(task_id="accurate", bash_command="echo 'accurate'")
    inaccurate = BashOperator(task_id="inaccurate", bash_command="echo 'inaccurate'")

    (
        [training_model_A, training_model_B, training_model_C]
        >> choose_best_model
        >> [accurate, inaccurate]
    )
