FROM python:3.9-slim-buster
LABEL MAINTAINER="Intechideas International"
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY src/requirements/base.txt base.txt
COPY src/requirements/development.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ /code/
RUN adduser --disabled-password --gecos '' deploy

# CMD ["celery", "-A", "src.apps.profiles", "worker", "--loglevel=INFO"]
