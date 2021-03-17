import requests

from uuid import UUID

from fastapi import FastAPI, Request, Response, Header, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Optional

from app.constants import identity, authorization, bond_host
from app.handlers import plaid_bond_test, create_link_token, create_access_token, plaid_bond_micro_deposit_test, update_link_token

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


@app.get("/plaid/create_link_token/{account_id}")
def get_link_token(account_id):
    """    
    Gets a link token.

    Use "plaid"  as the account_id to call plaid's API "link/token/create" directly,
    submit a valid account_id instead to use Bond's API.
    """
    return create_link_token(account_id)

@app.patch("/plaid/update_link_token/{account_id}")
def patch_link_token(account_id, data:dict):
    """    
    Gets a link token.

    Use "plaid"  as the account_id to call plaid's API "link/token/create" directly,
    submit a valid account_id instead to use Bond's API.
    """
    return update_link_token(account_id, data)


@app.get("/plaid/{account_id}")
async def get_html(account_id):
    """
    Gets a HTML page which 
    1. creates a link token 
    2. initializes a Plaid Link Object (PLO) using the link token
    3. exchanges the  public token from the PLO to get an access token

    Use "plaid"  as the account_id to call plaid's API directly,
    submit a valid account_id instead to use Bond's API.
    """
    return Response(content=plaid_bond_test(account_id))

@app.get("/plaid/{account_id}/{linked_account_id}")
async def get_html_manual_microdeposit(account_id, linked_account_id):
    """
    Gets a HTML page which verifies the microdeposits to an account

    Use "plaid"  as the account_id to call plaid's API directly,
    submit a valid account_id instead to use Bond's API.
    """
    return Response(content=plaid_bond_micro_deposit_test(account_id, linked_account_id))

@app.post("/plaid/create_access_token/{account_id}")
def post_access_token(account_id, data:dict):
    """    
    Gets an access token.

    Use "plaid"  as the account_id to call plaid's API "item/public_token/exchange" directly,
    submit a valid account_id instead to use Bond's API.
    """
    return create_access_token(account_id, data)


