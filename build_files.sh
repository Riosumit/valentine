echo " BUILD START"
python3.9 -m pip install django
python3.9 -m pip install mysql_connector
python3.9 manage.py collectstatic --noinput --clear
echo " BUILD END"