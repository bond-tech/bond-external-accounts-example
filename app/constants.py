from os import environ
from os.path import exists
from dotenv import load_dotenv

# load .env file if it exists (not under systemd or kubernetes)
if exists(".env"):
    load_dotenv()

identity = environ.get("IDENTITY", None)
authorization = environ.get("AUTHORIZATION", None)

bond_host = "https://sandbox.bond.tech"
plaid_host = "https://sandbox.plaid.com"

api_docs = "https://docs.bond.tech/reference"

PLAID_CLIENT_ID = environ.get("PLAID_CLIENT_ID", None)
PLAID_SECRET = environ.get("PLAID_SECRET", None)
PLAID_PRODUCTS = environ.get("PLAID_PRODUCTS", "transactions")
PLAID_COUNTRY_CODES = environ.get("PLAID_COUNTRY_CODES", "US")
PLAID_ENV = environ.get("PLAID_ENV", "sandbox")
