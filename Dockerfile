FROM python:3.8 AS main
COPY . /bowling
WORKDIR /bowling

FROM main AS dev
COPY --from=main /bowling .
RUN pip3 install -U pip && pip3 install -r requirements-dev.txt

CMD ["python3", "main.py"]
