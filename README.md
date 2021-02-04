
Demo utilizing the Plaid SDK https://plaid.com/docs/link/web/#installation

Mimics the card demo here: https://github.com/bond-tech/bond-sdk-card-demo

Maintainer(s): @adityaatbond. 

# Introduction

This is a simple demo service showing how to run the Plaid SDK with a Bond backend. Particularly, the demo shows how a Brand might integrate with Plaid and Bond to link a Bank to a Card and unlock ACH capabilities. 

Built on [FastAPI](https://fastapi.tiangolo.com/). Run under [`unvicorn`](https://www.uvicorn.org/) or [`gunicorn`](https://gunicorn.org/) with a [`unvicorn` worker](https://www.uvicorn.org/#running-with-gunicorn). 

## Running Locally

To run locally, clone the repo and run
```
poetry install && poetry update
poetry run uvicorn app:app --port=8001 --reload
```
(Leave off `--reload` if you don't want code changes to spark server reloads.)  Open a browser to 
```
http://localhost:8001/plaid/<account_id>
```
where `account_id` is a valid Bond account ID. 

The API documentation: 
```
http://localhost:8001/docs
```

The following environment variables are needed:
```
PLAID_CLIENT_ID
PLAID_SECRET
PLAID_PRODUCTS
PLAID_COUNTRY_CODES
PLAID_ENV
```
Contact @adityaatbond for these.

# Discussion

The basic approach here is to serve `html` content that calls back to the server to get a one-time token used by in-browser `javascript`. This demonstrates that you can secure your credentials in your server infrastructure, and use those to generate and supply the temporary keys within content served to card holders. Of course, your content delivery may not itself be delivered by your service layer, maybe by a CDN. This is just a convenient construct in this demo. 

