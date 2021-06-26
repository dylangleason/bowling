FROM python:3.8

COPY . /bowling
WORKDIR /bowling

CMD ["python3", "main.py"]
