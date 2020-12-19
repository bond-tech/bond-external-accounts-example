
import requests

from uuid import UUID

from fastapi import FastAPI, Request, Response, Header, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from typing import Optional

from app.constants import (
    identity , authorization , bond_host
)
from app.handlers  import (
    card_view_page , create_token
)

app = FastAPI()

@app.get("/health")
async def health():

    # verify bond's auth service is reachable
    url = f"{bond_host}/auth/health/alive"
    r = requests.get(url)
    if r.status_code != 200: 
        raise HTTPException(status_code=500, detail="Bond's auth service isn't reachable")

    # verify key permissions for making one time tokens
    url = f"{bond_host}/api/v0/auth/"
    head = {
        'Identity': identity , 
        'Authorization': authorization , 
        'X-BaaS-Service': 'auth',
        'X-BaaS-Route': '/key/temporary',
        'X-BaaS-Method': 'post',
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

