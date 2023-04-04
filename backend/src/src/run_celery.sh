#!/bin/sh

# wait for redis server to start
sleep 10

# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m deploy -c "celery -A src.celery worker -Q default -n default@%h"