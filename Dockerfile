# syntax=docker/dockerfile:1
FROM python:3.6-alpine
WORKDIR .
ENV FLASK_APP=us_src/unisearch/app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
CMD ["gunicorn", "--bind", "0.0.0.0:5000" "unisearch.app:app"]