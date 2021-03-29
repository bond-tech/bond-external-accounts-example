from os import environ
from os.path import exists
from dotenv import load_dotenv

# load .env file if it exists (not under systemd or kubernetes)
if exists(".env"):
    load_dotenv()

identity = environ.get("IDENTITY", None)
authorization = environ.get("AUTHORIZATION", None)

# can be production, sandbox
PLAID_ENV = environ.get("PLAID_ENV","sandbox")

# can be sandbox.dev, api.dev, sandbox(prod), api(prod), 
# api.staging, sandbox.staging.
BOND_ENV = environ.get("BOND_ENV","sandbox")

plaid_host = f"https://{PLAID_ENV}.plaid.com"
bond_host = f"https://{BOND_ENV}.dev.bond.tech"

api_docs = "https://docs.bond.tech/reference"

PLAID_CLIENT_ID=environ.get("PLAID_CLIENT_ID",None)
PLAID_SECRET=environ.get("PLAID_SECRET", None)
PLAID_PRODUCTS=environ.get("PLAID_PRODUCTS","transactions")
PLAID_COUNTRY_CODES=environ.get("PLAID_COUNTRY_CODES","US")
PLAID_ENV=environ.get("PLAID_ENV", "sandbox")
