#!/bin/bash
python3 manage.py check && \
python3 manage.py collectstatic --noinput && \
python3 manage.py makemigrations && \
python3 manage.py migrate && \
python3 manage.py runserver 0.0.0.0:8033
#python3 manage.py runserver localhost:8000