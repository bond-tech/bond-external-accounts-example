from os import environ
from os.path import exists
from dotenv import load_dotenv

# load .env file if it exists (not under systemd or kubernetes)
if exists(".env"):
    load_dotenv()

identity = environ.get("IDENTITY","f2ced16a-463a-48e9-931d-25120809041f")
authorization = environ.get("AUTHORIZATION","gsPjke9IgM2SfvrTzExLilVtK2b6Qigmgb5YMsfgBn0LWo6PhL09I4AX3uAYy4Wc")

bond_host = "https://sandbox.bond.tech"

sdk_docs = "https://docs.bond.tech/docs/retrieve-card-details-set-pins-and-reset-pins"
api_docs = "https://docs.bond.tech/reference"

PLAID_CLIENT_ID=environ.get("PLAID_CLIENT_ID","5f91a184df1def00129064d3")
PLAID_SECRET=environ.get("PLAID_SECRET","f82599de2db1661a229e24854dff14")
PLAID_PRODUCTS=environ.get("PLAID_PRODUCTS","transactions")
PLAID_COUNTRY_CODES=environ.get("PLAID_COUNTRY_CODES","US")
PLAID_ENV=environ.get("PLAID_ENV", "sandbox")