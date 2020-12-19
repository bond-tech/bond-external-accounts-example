
Demo utilizing the Bond web SDK ([repo](https://github.com/bond-tech/bond-sdk-cards), [cdn](https://cdn.bond.tech/sdk/cards/v1/bond-sdk-cards.js)) for card presentment and PIN functionality. 

Maintainer(s): @rossatbond. 

# Introduction

This is a simple demo service showing how to run the Bond Card SDK with a backend. Particularly, the demo shows how you might include a method in your backend to pass back valid temporary keys (or "one time tokens") to allow your cardholders to securely access their card details, without exposing your own Bond credentials on the web. 

Built on [FastAPI](https://fastapi.tiangolo.com/). Run under [`unvicorn`](https://www.uvicorn.org/) or [`gunicorn`](https://gunicorn.org/) with a [`unvicorn` worker](https://www.uvicorn.org/#running-with-gunicorn). 

## Running Locally

To run locally, clone the repo and run
```
poetry install && poetry update
poetry run uvicorn app:app --port=8000 --reload
```
(Leave off `--reload` if you don't want code changes to spark server reloads.)  Open a browser to 
```
http://localhost:8000/card/view/<card_id>
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
http://localhost:8000/card/view/<card_id>
```
where `card_id` is a valid Bond card ID. 

# Discussion

The basic approach here is to serve `html` content that calls back to the server to get a one-time token used by in-browser `javascript`. This demonstrates that you can secure your credentials in your server infrastructure, and use those to generate and supply the temporary keys within content served to card holders. Of course, your content delivery may not itself be delivered by your service layer, maybe by a CDN. This is just a convenient construct in this demo. 
