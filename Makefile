default: build run

build:
	docker build -t 'dylangleason:bowling' .

run:
	docker run --rm -it 'dylangleason:bowling' python3 bowling.py

test:
	docker run --rm 'dylangleason:bowling' python3 -m unittest -v

clean:
	docker image rm 'dylangleason:bowling'
