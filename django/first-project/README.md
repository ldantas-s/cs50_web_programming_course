# Project info

## docker commands

how to stop all docker containers

```bash
docker stop $(docker ps -a -q)
```

to start container

```bash
docker-compose up
```

to start containers in background

```bash
docker-compose up -d
```

to see container running

```bash
docker container ls
```

how to run the terminal inside of container

```bash
docker exec -it [container_id] /bin/sh
```

## to create a new django app

```bash
python manage.py startapp [appName]
```

how to generate the requirements.txt

```bash
pip freeze > requirements.txt
```
