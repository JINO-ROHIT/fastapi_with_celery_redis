ABSOLUTE_PATH := ${shell pwd}

.PHONY: serve
serve:
	docker compose up --build

.PHONY: stop
stop:
	docker compose down