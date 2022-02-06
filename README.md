![example workflow](https://github.com/fibboo/books_db_flask/actions/workflows/workflow.yaml/badge.svg)

# Flask Book DB (in production)
## About:
This project is my way to understand Flask, SQLAlchemy, Alembic, Pytest,
Flask-Login and Flask-JWT
<br>
There are two main apps:
- Standard web app on HTML templates. Anonymous user can look all books
and authors in DB, sign up and log in. Authenticated user can create
new books and authors, update and delete self, books, authors that created.
- RESTful API. Anonymous user can get all users, books and authors in DB,
create new user, get auth token. Authenticated user can create
new books and authors, update and delete self, books, authors that created.
<br>
When you run project (how to do it a bit later), you can look documentation
on API here http://localhost/api/docs/

## To-do
- Optimise views, serializers, and validator. DRY is violated in several places.
It would be optimal to rewrite 'api' app on Flask-RESTful.
- Complete documentation for REST API. There are places where it's not accurate
  (no nested related objects in response examples).
- Complete test. Coverage is minimal now.

## Requirements:
python 3.8 <br>
docker https://docs.docker.com/engine/install/ <br>
docker-compose https://docs.docker.com/compose/install/

## How to run:

Clone project and cd to infra
```
git clone git@github.com:fibboo/books_db_flask
```
cd to book_infra/ folder, create .env file as in the template
books_infra/.env.template and run project in docker.
```
cd book_infra/
cp .env.template .env
nano .env  # change data
sudo docker-compose up -d
```
For the first run make migrate
```
sudo docker-compose exec web flask db upgrade
```

## Pushing, GitHub Actions
Create secrets in GitHub repository for Actions to work properly
```text
DOCKER_USERNAME
DOCKER_PASSWORD
TELEGRAM_TO
TELEGRAM_TOKEN
```
Push. GitHub actions will check for PEP8, make all test and if it's ok will
push image to DockerHub