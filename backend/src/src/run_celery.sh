#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m deploy -c "celery -A apps.profiles.celery worker -Q default -n default@%h"