dev:
	sudo docker-compose -p hsb -f local.yml up

build:
	sudo docker-compose -p hsb -f local.yml build

migrations:
	docker-compose -p hsb -f local.yml run --rm django python manage.py makemigrations

migrate:
	docker-compose -p hsb -f local.yml run --rm django python manage.py migrate

superuser:
	docker-compose -p hsb -f local.yml run --rm django python manage.py createsuperuser

shell:
	docker-compose -p hsb -f local.yml run --rm django python manage.py shell
