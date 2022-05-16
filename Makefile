.ONESHELL:
.SHELLFLAGS += -e

f:
	cd frontend
	npm run serve

b:
	cd backend && \
	source env/bin/activate && \
	python3 manage.py runserver 0.0.0.0:8000

