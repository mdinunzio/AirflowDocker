import datetime
import os
import sys

import pendulum
from airflow.decorators import dag, task
from airflow.models.baseoperator import chain

sys.path.append(r"/opt/airflow/code/finances")

import finances.io.ynab
from finances.job.text_discretionary import RECIPIENT, TODAY

AMERICA_NEW_YORK = pendulum.timezone("America/New_York")
AIRFLOW_EMAIL_ALERT_LIST = os.environ["AIRFLOW_EMAIL_ALERT_LIST"]
AIRFLOW_PYTHON_EXECUTABLE = os.environ["AIRFLOW_PYTHON_EXECUTABLE"]


@dag(
    schedule="30 10 * * *",
    start_date=datetime.datetime(2024, 10, 15, 10, 30, 0, 0, tzinfo=AMERICA_NEW_YORK),
    catchup=False,
    tags=["ynab"],
    default_args={
        "email": AIRFLOW_EMAIL_ALERT_LIST,
        "email_on_failture": True,
        "email_on_retry": False,
        "retries": 2,
        "retry_delay": datetime.timedelta(minutes=30),
    },
)
def text_discretionary():

    @task
    def fetch_single_date_budget_frame():
        budget = finances.io.ynab.fetch_single_date_budget_frame(
            TODAY.year, TODAY.month
        )
        return budget

    @task.external_python(python=r"/opt/airflow/envs/finances/bin/python")
    def get_discretionary_budget(budget):
        import sys

        sys.path.append(r"/opt/airflow/code/finances")
        discretionary = finances.job.text_discretionary.get_discretionary_budget(budget)
        return discretionary

    @task
    def render_email_body(discretionary):
        body = finances.job.text_discretionary.render_email_body(discretionary)
        return body

    @task
    def send_email(body):
        finances.io.gmail.send(recipient=RECIPIENT, body=body)

    budget = fetch_single_date_budget_frame()
    discretionary = get_discretionary_budget(budget)
    body = render_email_body(discretionary)
    send_email(body)


text_discretionary()
