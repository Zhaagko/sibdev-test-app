run:
	./manage.py runserver 0.0.0.0:8000

migrate:
	./manage.py migrate

bash:
	docker-compose exec -it web bash