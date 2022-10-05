# Airline System

## How to initiate a django project with docker

[link](https://docs.docker.com/samples/django/)

```bash
  $sudo docker-compose up [name_service] django-admin startproject [app_name] .
```

> in case of problems about permission, to run:

```bash
  $sudo chown -R $USER:$USER [app_name] manage.py
```

## How to create a django super user

```bash
  $python manage.py createsuperuser
```
