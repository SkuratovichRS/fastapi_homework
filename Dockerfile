FROM python:3.12-slim-bookworm

WORKDIR /workdir

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY app app

ENV PYTHONPATH=/workdir

