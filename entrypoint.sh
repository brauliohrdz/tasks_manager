echo -e "Iniciando Django ..."
python ./manage.py makemigrations;
python ./manage.py migrate;
python ./manage.py runserver 0.0.0.0:9000;