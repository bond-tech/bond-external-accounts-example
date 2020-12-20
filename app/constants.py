
from os import environ
from os.path import exists
from dotenv import load_dotenv

# load .env file if it exists (not under systemd or kubernetes)
if exists('.env'): 
    load_dotenv()

identity      = environ['IDENTITY'] 
authorization = environ['AUTHORIZATION']

bond_host = "https://api.bond.tech"

sdk_docs = "https://docs.bond.tech/docs/retrieve-card-details-set-pins-and-reset-pins"
api_docs = "https://docs.bond.tech/reference"
