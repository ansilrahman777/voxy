#!/bin/bash

# Install dependencies and migrate DB
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate

# # Auto-create superuser if it doesn't exist
# python manage.py shell <<EOF
# import os
# from django.contrib.auth import get_user_model

# User = get_user_model()
# email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
# username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
# first_name = os.environ.get('DJANGO_SUPERUSER_FIRSTNAME')
# last_name = os.environ.get('DJANGO_SUPERUSER_LASTNAME')
# mobile = os.environ.get('DJANGO_SUPERUSER_MOBILE')
# password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

# if email and not User.objects.filter(email=email).exists():
#     User.objects.create_superuser(
#         email=email,
#         username=username,
#         first_name=first_name,
#         last_name=last_name,
#         mobile=mobile,
#         password=password
#     )
# EOF
