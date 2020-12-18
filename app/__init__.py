from fastapi import FastAPI, Request, Response, Header, Depends, HTTPException

import requests

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
async def get_customer_token(customer_id: str):
    url = "https://api.bond.tech/api/v0/auth/key/temporary"
    data = {"customer_id":customer_id}
    head = {
        'Identity': identity , 
        'Authorization': authorization , 
        'Content-type': 'application/json' ,
    }
    r = requests.post(url, headers=head, json=data)
    if r.status_code in [200,201]: 
        return r.json()
    raise HTTPException(detail="failed to create token", status_code=500)

@app.get("/{customer_id}/{card_id}")
async def get_html_both(customer_id: str, card_id: str):
    html = format_page(customer_id, card_id)
    return Response(content=html)

@app.get("/{card_id}")
async def get_html_card(card_id: str):
    html = format_page(default_customer_id, card_id)
    return Response(content=html)

