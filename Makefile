.PHONY: build purgedb run stop

build: clean stop purgedb
	mkdir -p '.data/db'
	docker-compose up -d --build
	docker-compose exec orderserviceopply python manage.py makemigrations
	docker-compose exec orderserviceopply python manage.py migrate
	docker-compose exec orderserviceopply python manage.py loaddata default_admin.json
	docker-compose kill orderserviceopply db_opply test

purgedb:
	echo "Removing all Data from DB"
	- docker rm order_service_opply_db

clean:
	rm -rf .data

run:
	docker-compose up

stop:
	docker-compose kill orderserviceopply db_opply test