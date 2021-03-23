
Demo utilizing the Plaid SDK https://plaid.com/docs/link/web/#installation

Maintainer(s): aditya@bond.tech 

# Introduction

This is a simple demo service showing how to run the Plaid SDK with a Bond backend. Particularly, the demo shows how a Brand might integrate with Plaid and Bond to link a Bank to a Card and unlock ACH capabilities. 

Built on [FastAPI](https://fastapi.tiangolo.com/). Run under [`unvicorn`](https://www.uvicorn.org/) or [`gunicorn`](https://gunicorn.org/) with a [`unvicorn` worker](https://www.uvicorn.org/#running-with-gunicorn). 

## Running Locally

To run locally, clone the repo and run
```
poetry install && poetry update
poetry run uvicorn app:app --port=8001 --reload
```
(Leave off `--reload` if you don't want code changes to spark server reloads.)  

### Link account:

Open a browser to 
```
http://localhost:8001/plaid/<account_id>
```
where `account_id` is a valid Bond account ID. 

Be sure to define your Bond API keys as environment variables:
```
IDENTITY
AUTHORIZATION
```

This process links a Bond account (`account_id`) to an external bank account (`linked_account_id`).


Use plaid in instead of a Bond account_id to directly hit plaid's endpoints instead.

```
http://localhost:8001/plaid/plaid
```

The following environment variables are needed if using plaid's sandbox directly (Please see https://plaid.com/docs/quickstart/ and https://dashboard.plaid.com/overview/sandbox):
```
PLAID_CLIENT_ID
PLAID_SECRET
PLAID_PRODUCTS
PLAID_COUNTRY_CODES
PLAID_ENV
```
### Initiate manual microdeposit verification flow (same-day micro deposit flow)
To initiate the microdeposit flow, use a username and password 
other than `user_good` and `pass_good` during the account linking process.
You'll be prompted to "Link with account numbers".
Follow the steps in the plaid flow and enter the following values
routing number: 110000000 | account number: 1111222233330000 when prompted.

Notice in the console that the account verification_status is set to `pending_manual_verification`.

### Verify microdeposits
Open a browser to 
```
http://localhost:8001/plaid/<account_id>/<linked_account_id>
```
where `account_id` is a valid Bond account ID and `linked_account_id` is the linked external account_id 
which is obtained by the link account step (check console to get the linked_account_id).

In the sandbox environment, a confirming the values of $0.01 and $0.02 a the two microdeposits would 
successfully verify the microdeposit flow. Any other values for the microdeposits would fail to verify
the linked external account.

### Other information

Be sure to define your Bond API keys as environment variables:
```
IDENTITY
AUTHORIZATION
```

The API documentation: 
```
http://localhost:8001/docs
```

Contact aditya@bond.tech for any questions.

Please refer to the docs (https://docs.bond.tech/docs/link-external-accounts) for more details. Also check the web browser console log for other details about the linking process.


# Discussion

The basic approach here is to serve `html` content that calls back to the server to get a one-time token used by in-browser `javascript`. This demonstrates that you can secure your credentials in your server infrastructure, and use those to generate and supply the temporary keys within content served to card holders. Of course, your content delivery may not itself be delivered by your service layer, maybe by a CDN. This is just a convenient construct in this demo. 

