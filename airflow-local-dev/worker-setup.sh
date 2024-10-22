#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Create a virtual environments
mkdir /opt/airflow/envs
python -m venv /opt/airflow/envs/finances
/opt/airflow/envs/finances/bin/python -m pip install -r /opt/airflow/requirements/requirements-finance.txt

# Start the celery worker
celery worker