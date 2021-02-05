from os import environ
from os.path import exists
from dotenv import load_dotenv

# load .env file if it exists (not under systemd or kubernetes)
if exists(".env"):
    load_dotenv()

identity = environ.get("IDENTITY","2c22f625-0f11-473d-b583-27e1d1a5770c")
authorization = environ.get("AUTHORIZATION","JPJoe2metlnKbrlXaLK555PSQPHwY/o1fc1FIhAvt56xg7ozzFnv8l+2Cas5yXGe")

bond_host = "https://sandbox.dev.bond.tech"
plaid_host = "https://sandbox.plaid.com"

api_docs = "https://docs.bond.tech/reference"

PLAID_CLIENT_ID=environ.get("PLAID_CLIENT_ID","5f91a184df1def00129064d3")
PLAID_SECRET=environ.get("PLAID_SECRET","f82599de2db1661a229e24854dff14")
PLAID_PRODUCTS=environ.get("PLAID_PRODUCTS","transactions")
PLAID_COUNTRY_CODES=environ.get("PLAID_COUNTRY_CODES","US")
PLAID_ENV=environ.get("PLAID_ENV", "sandbox")