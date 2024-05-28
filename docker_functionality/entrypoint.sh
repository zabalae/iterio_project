#!/bin/bash

# Wait for the MySQL database container to be ready
./wait-for-it.sh db:3306 -t 30

# Run Django migrations and start the Django application
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
