WORKON_HOME ?= venv

default: build run

build:
	docker build -t 'dylangleason:bowling' .

run:
	docker run --rm -it 'dylangleason:bowling'

test:
	docker run --rm 'dylangleason:bowling' python3 -m unittest -v

venv:
	python -m venv $(WORKON_HOME)/bowling

clean:
	docker image rm 'dylangleason:bowling'
