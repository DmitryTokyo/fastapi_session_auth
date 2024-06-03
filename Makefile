migrate:
	alembic upgrade head

runserver:
	uvicorn src.server:app --reload --port 5000

ipython:
	ipython -i ipython_startup.py

style:
	flake8 .

types:
	mypy --no-error-summary .

check:
	make -j2 style types

tests:
	python -m pytest -vvs