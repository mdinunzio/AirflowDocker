import datetime
import pendulum
import sys

from airflow.decorators import dag, task
from airflow.models.baseoperator import chain

sys.path.append(r"/opt/airflow/code/finances")

import finances.io.ynab
from finances.job.text_discretionary import RECIPIENT, TODAY


america_new_york = pendulum.timezone("America/New_York")


@dag(
    schedule="30 10 * * *",
    start_date=datetime.datetime(2024, 10, 16, 10, 30, 0, 0, tzinfo=america_new_york),
    catchup=False,
    tags=["ynab"],
)
def text_discretionary():

    @task
    def fetch_single_date_budget_frame():
        budget = finances.io.ynab.fetch_single_date_budget_frame(
            TODAY.year, TODAY.month
        )
        return budget

    @task
    def get_discretionary_budget(budget):
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
