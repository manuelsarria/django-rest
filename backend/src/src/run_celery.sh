# run Celery worker for our project myproject with Celery configuration stored in Celeryconf
su -m deploy -c "celery -A src.celery worker -Q default -n default@%h && celery -A src.celery beat -l info"

sleep 5

su -m deploy -c "celery -A apps.profiles.tasks worker --loglevel=info"