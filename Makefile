_django_user = django
_execc = docker-compose exec
_django_execc = docker-compose exec --user=$(_django_user) app

show_queue:
	$(_execc) rabbitmq rabbitmqctl list_queues name messages_ready messages_unacknowledged

migrate:
	$(_django_execc) python manage.py migrate

pip_install:
	$(_execc) --user=root app pip3 install -r requirements.txt

test:
	$(_django_execc) python manage.py test

run_sender:
	$(_django_execc) python sender.py
