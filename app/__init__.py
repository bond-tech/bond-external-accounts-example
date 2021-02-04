import requests

from uuid import UUID

from fastapi import FastAPI, Request, Response, Header, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Optional

from app.constants import identity, authorization, bond_host
from app.handlers import plaid_bond_test, create_link_token

app = FastAPI()


@app.get("/health")
async def health():

    # verify bond's auth service is reachable
    url = f"{bond_host}/auth/health/alive"
    r = requests.get(url)
    if r.status_code != 200:
        raise HTTPException(
            status_code=500, detail="Bond's auth service isn't reachable"
        )

    # verify key permissions for making one time tokens
    url = f"{bond_host}/api/v0/auth/"
    head = {
        "Identity": identity,
        "Authorization": authorization,
        "X-BaaS-Service": "auth",
        "X-BaaS-Route": "/key/temporary",
        "X-BaaS-Method": "post",
    }
    r = requests.get(url, headers=head)
    if r.status_code != 200:
        raise HTTPException(status_code=500, detail="You cannot create temporary keys")

    # the one-time tokens will have permissions for the actual card routes
    # so we don't need to check those


app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/token/{customer}")
async def get_customer_token(customer: UUID):
    return create_token(customer)


@app.get("/accounts/{account_id}/create-link-token")
async def get_create_token(customer: UUID):
    return create_token(customer)

@app.get("/card/view/{card}")
async def get_html_card(card: UUID, customer: Optional[UUID] = None):
    if customer is None:
        customer = card
    return Response(content=card_view_page(customer, card))


@app.get("/card/pin/view/{card}")
async def get_html_card(card: UUID, customer: Optional[UUID] = None):
    raise HTTPException(status_code=501)


@app.get("/card/pin/set/{card}")
async def get_html_card(card: UUID, customer: Optional[UUID] = None):
    raise HTTPException(status_code=501)


@app.get("/card/pin/reset{card}")
async def get_html_card(card: UUID, customer: Optional[UUID] = None):
    raise HTTPException(status_code=501)

@app.get("/plaid/create_link_token")
def get_link_token():
    # Get the client_user_id by searching for the current user
    # user = User.find(...)
    # client_user_id = "random_user"
    # url = "https://sandbox.plaid.com" + "/link/token/create"
    # # Create a link_token for the given user


    
    # response = client.LinkToken.create({
    #   'user': {
    #     'client_user_id': client_user_id,
    #   },
    #   'products': ['transactions'],
    #   'client_name': 'My App',
    #   'country_codes': ['US'],
    #   'language': 'en',
    #   'webhook': 'https://webhook.sample.com',
    # })

    # link_token = response['link_token']
    # Send the data to the client
    return create_link_token("sda")
    # return {
    #     "link_token": "link-sandbox-740f6e76-20e1-4690-b730-6164da554542",
    #     "expiration": "2021-01-27T23:29:06Z",
    #     "linked_account_id": "1a130d45-3dc3-4c58-b0d8-9784aae0d009",
    #     "status": "link initiated"
    # }

@app.get("/plaid/{account_id}")
async def get_html_test(account_id):
    return Response(content=plaid_bond_test(account_id))


