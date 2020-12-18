
from os import environ
from os.path import exists
from dotenv import load_dotenv

# load .env file if it exists (not under systemd or kubernetes)
if exists('.env'): 
    load_dotenv()

identity      = environ['IDENTITY'] 
authorization = environ['AUTHORIZATION']

default_customer_id = "7ee10cfa-07c2-48ac-928d-5ab41a5e216f"


