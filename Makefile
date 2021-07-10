VIRTUAL_ENV ?= $(HOME)/.local/share/virtualenvs/bowling

default: build run

build:
	docker build -t 'dylangleason:bowling' .

clean:
	docker image rm 'dylangleason:bowling'

run:
	docker run --rm -it 'dylangleason:bowling'

test:
	docker run --rm 'dylangleason:bowling' python3 -m unittest -v

type-check:
	docker run --rm 'dylangleason:bowling' mypy .

venv:
	python3 -m venv $(VIRTUAL_ENV) && . $(VIRTUAL_ENV)/bin/activate && pip install -r requirements-dev.txt
