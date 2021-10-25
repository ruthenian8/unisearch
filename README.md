# Unisearch

## Overview
The program crawls all links from a given webpage.

The deepness of crawling is 1, e.g. it is required that each link contains a part of the corpus to build.

After building the corpus is done, fulltext search
can be performed via the API.

The pages to parse are assumed to have their text wrapped in p-tags.
Primary target is lib.ru or static news web apps.

## Reqirements
### Deployment with Docker
* Docker
* Docker-compose
### Local deployment
* See requirements.txt
* Note: ASGI Flask app is deployed with Gunicorn, which is linux-specific.
* Note: you might want to alter the database connection parameters in the config, when working in a non-isolated environment.

## Usage
### Commands
If deployed successfully, the app listens to port 5000 on localhost. The API basically has two endpoints.
* /parse - GET. Param "url" must be the full http address of the target page. Requests to this endpoint should be made to start the app logic.
* / - GET. Param "query" should contain the words to search with any delimiter, e.g. "мама,рама" is fine. Returns an error if nothing has been parsed.
* You can also invoke tox or pytest to run the testing routines, e.g. 
```shell
pytest .
```

### Example
```shell
docker-compose up
curl 0.0.0.0:5000/parse?url=https://shalamov.ru/library/1/
curl 0.0.0.0:5000/?query=прииск
```