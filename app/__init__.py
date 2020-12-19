from fastapi import FastAPI, Request, Response, Header, Depends, HTTPException
from typing import Optional

import requests

from uuid import UUID

from app.handlers  import *
from app.payloads import *
from app.constants import *

app = FastAPI()

@app.get("/health")
async def health():
    return {}

@app.get("/token")
async def get_default_token():
    url = "https://api.bond.tech/api/v0/auth/key/temporary"
    data = {"customer_id":default_customer_id}
    head = {
        'Identity': identity , 
        'Authorization': authorization , 
        'Content-type': 'application/json' ,
    }
    r = requests.post(url, headers=head, json=data)
    if r.status_code in [200,201]: 
        return r.json()
    raise HTTPException(detail="failed to create token", status_code=500)

@app.get("/token/{customer_id}")
async def get_customer_token(customer_id: UUID):
    url = "https://api.bond.tech/api/v0/auth/key/temporary"
    data = {"customer_id":str(customer_id)}
    head = {
        'Identity': identity , 
        'Authorization': authorization , 
        'Content-type': 'application/json' ,
    }
    r = requests.post(url, headers=head, json=data)
    if r.status_code in [200,201]: 
        return r.json()
    raise HTTPException(detail="failed to create token", status_code=500)

@app.get("/{card}")
async def get_html_card(card: UUID, customer: Optional[UUID] = None):
    if customer is None: 
        customer = card
    return Response(content=format_page(customer, card))

