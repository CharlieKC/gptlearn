SHELL := /bin/zsh
# Makefile to manage Django, Express, and Nginx services

BASE_DIR=$(shell pwd)

# Django-related variables
DJANGO_DIR=${BASE_DIR}/backend

# Express-related variables
EXPRESS_DIR=${BASE_DIR}/frontend

# nginx conf file
NGINX_CONF=${BASE_DIR}/nginx/nginx.conf

# Targets

all: start_django start_express

start_django:
	@echo "Starting Django project..."
	@cd $(DJANGO_DIR) && \
	poetry run uvicorn flashcards.asgi:application --host 0.0.0.0 --reload &&

stop_django:
	@echo "Stopping Django project..."
	@kill `cat $(GUNICORN_PID)` || true

start_express:
	@echo "Starting Express project..."
	@cd $(EXPRESS_DIR) && \
	npm run dev

stop_express:
	@echo "Stopping Express project..."
	@kill `cat $(EXPRESS_PID)` || true

start_nginx:
	@echo "Starting Nginx..."
	@nginx -c $(NGINX_CONF)

stop_nginx:
	@echo "Stopping Nginx..."
	@sudo nginx -s stop

restart_nginx:
	@echo "Restarting Nginx..."
	@sudo nginx -s reload

clean: stop_django stop_express stop_nginx

.PHONY: all start_django stop_django start_express stop_express start_nginx stop_nginx restart_nginx clean
