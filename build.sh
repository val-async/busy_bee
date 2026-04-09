#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input

PYTHONPATH=busy_bee_project python busy_bee_project/manage.py migrate
