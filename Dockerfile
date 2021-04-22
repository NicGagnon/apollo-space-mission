FROM python:3.7-slim-buster

WORKDIR /home/site/wwwroot

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock
RUN pip install pipenv
RUN pipenv install --dev --deploy --system

COPY . /home/site/wwwroot