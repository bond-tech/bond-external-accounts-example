
Demo utilizing the Bond web SDK ([repo](https://github.com/bond-tech/bond-sdk-cards), [cdn](https://cdn.bond.tech/sdk/cards/v1/bond-sdk-cards.js)) for card presentment and PIN functionality. 

Maintainer(s): @rossatbond. 

# Introduction

This is a simple demo service showing how to run the Bond Card SDK with a backend. Particularly, the demo shows how you might include a method in your backend to pass back valid temporary keys (or "tokens") to allow your cardholders to securely access their card details, without exposing your own credentials on the web. 

Built on [FastAPI](https://fastapi.tiangolo.com/). Run under [`unvicorn`](https://www.uvicorn.org/) or [`gunicorn`](https://gunicorn.org/) with a [`unvicorn` worker](https://www.uvicorn.org/#running-with-gunicorn). 

## Running Locally

To run locally, clone the repo and run
```
poetry install && poetry update
poetry run uvicorn app:app --port=8000 --reload
```
(Leave off `--reload` if you don't want code changes to spark server reloads.)  Open a browser to 
```
http://localhost:8000/<card_id>
```
where `card_id` is a valid Bond card ID. 

## Docker

Run in a `docker` container with the following: 
```
docker build . -t sdk-demo:local
docker run -e IDENTITY=<your identity> -e AUTHORIZATION=<your identity> -p 8000:8000 sdk-demo:local
``` 
Then open a browser to 
```
http://localhost:8000/<card_id>
```
where `card_id` is a valid Bond card ID. 

# Discussion

