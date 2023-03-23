cd .\TextWork
@echo off
start /B python manage.py runserver
start msedge http://127.0.0.1:8000/