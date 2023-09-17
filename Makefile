run:
	./manage.py runserver

migrate:
	./manage.py migrate

bash:
	docker-compose exec -it web bash