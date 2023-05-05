run:
	sudo docker-compose -p hsb -f local.yml up

stop:
	sudo docker-compose -p hsb -f local.yml stop

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

down:
	sudo docker-compose -p hsb -f local.yml down
