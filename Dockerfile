# syntax=docker/dockerfile:1
FROM python:3.7-alpine
WORKDIR .
ENV FLASK_APP=us_src/unisearch/app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
RUN apk add --no-cache build-base libffi-dev libressl-dev
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apk del libffi-dev libressl-dev musl-dev
EXPOSE 5000
COPY . .
RUN pip install -e .
#CMD sh -c 'env'
CMD sh -c 'gunicorn --bind 0.0.0.0:5000 --timeout 360 unisearch.app:app'