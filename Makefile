.PHONY: run lint migrate check test verify install-hooks

run:
	uv run python manage.py runserver

lint:
	uv run djlint . --reformat

migrate:
	uv run python manage.py makemigrations && \
	uv run python manage.py migrate && \
	uv run python manage.py showmigrations

test:
	uv run python manage.py test apps.porfolio apps.services --settings=config.settings.test

check:
	uv run python manage.py check --settings=config.settings.test

verify: check test

install-hooks:
	git config core.hooksPath .githooks
	@echo "Git hooks enabled from .githooks"
