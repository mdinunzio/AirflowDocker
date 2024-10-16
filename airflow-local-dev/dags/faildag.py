import datetime
import pendulum

from airflow.decorators import dag, task

# Define the timezone
america_new_york = pendulum.timezone("America/New_York")

# Define your email recipients (can be a list)
email_recipients = ["youremail@example.com"]

# Default arguments for email notifications and retries
default_args = {
    "email": email_recipients,
    "email_on_failure": True,  # Send an email if a task fails
    "email_on_retry": False,  # Optional, email on retries
    "retries": 2,  # Retry once before failing
    "retry_delay": datetime.timedelta(seconds=1),  # Delay between retries
}


@dag(
    schedule=None,  # This DAG will not run automatically
    start_date=datetime.datetime(2024, 10, 15, tzinfo=america_new_york),
    catchup=False,
    tags=["test"],
    default_args=default_args,
)
def failing_dag():

    @task
    def divide_by_zero():
        # This task will fail due to division by zero
        return 1 / 0

    divide_by_zero()


failing_dag()
