dev:
	sudo docker-compose -f local.yml up

build:
	sudo docker-compose -f local.yml build

migrations:
	docker-compose -f local.yml run --rm django python manage.py makemigrations

migrate:
	docker-compose -f local.yml run --rm django python manage.py migrate

superuser:
	docker-compose -f local.yml run --rm django python manage.py createsuperuser
