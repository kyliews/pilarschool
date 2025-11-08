#!/bin/bash

pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# ADICIONE ESTA LINHA DE VOLTA
python manage.py createsuperuser --noinput