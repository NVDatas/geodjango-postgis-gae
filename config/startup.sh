#! /bin/sh

#####
# Django setup
#####
python app/manage.py migrate
python app/manage.py loaddata 001_geo_japan.json
echo "from django.contrib.auth import get_user_model; model = get_user_model(); u = model.objects.create_superuser('admin', 'admin@localhost', 'default') if model.objects.filter(username='admin').exists() == False else None" | python app/manage.py shell
