FROM python:3.10-slim-buster
LABEL MAINTAINER="Intechideas International"
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY src/requirements/base.txt base.txt
COPY src/requirements/development.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY src/ /code/
EXPOSE 8000
CMD bash -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"