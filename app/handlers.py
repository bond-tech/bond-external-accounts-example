import requests

from fastapi import HTTPException

from app.constants import *



def create_link_token(account_id):
    # Bond
    # url = f"https://api.dev.bond.tech/api/v0/accounts/{account_id}/external_accounts/plaid"
    # head = {
    #     "Identity": identity,
    #     "Authorization": authorization,
    #     "Content-type": "application/json",
    # }

    url = f"https://sandbox.plaid.com/link/token/create"
    headers = {
      "Content-type": "application/json",
    }
    payload = {
      "client_id": PLAID_CLIENT_ID,
      "secret": PLAID_SECRET,
      "user": {"client_user_id": "bond"},
      "client_name": "Plaid App",
      "products": ["auth"],
      "country_codes": ["US"],
      "language": "en",
      "account_filters": {
        "depository": {
            "account_subtypes": ["checking"]
        }
      }
    }
    r = requests.post(url=url, headers = headers, json=payload)
    return r.json()

    # 
    # url = f"https://api.dev.bond.tech/api/v0/accounts/{account_id}/external_accounts/plaid"
    # head = {
    #     "Identity": identity,
    #     "Authorization": authorization,
    #     "Content-type": "application/json",
    # }

    # configs = {
    #   'user': {
    #       'client_user_id': '123-test-user-id',
    #   },
    #   'products': ['auth', 'transactions'],
    #   'client_name': "Plaid Test App",
    #   'country_codes': ['GB'],
    #   'language': 'en',
    #   'webhook': 'https://sample-webhook-uri.com',
    #   'link_customization_name': 'default',
    #   'account_filters': {
    #       'depository': {
    #           'account_subtypes': ['checking', 'savings'],
    #       },
    #   },
    # }
    # # create link token
    # response = client.LinkToken.create(configs)
    # link_token = response['link_token']
    # return {
    #     "link_token": "link-sandbox-740f6e76-20e1-4690-b730-6164da554542",
    #     "expiration": "2021-01-27T23:29:06Z",
    #     "linked_account_id": "1a130d45-3dc3-4c58-b0d8-9784aae0d009",
    #     "status": "link initiated"
    # }
    # r = requests.get(url, headers=head)
    # if r.status_code in [200, 201]:
    #     return r.json()
    # raise HTTPException(status_code=500, detail="failed to create linked token")

def create_token(customer):
    url = "https://sandbox.bond.tech/api/v0/auth/key/temporary"
    data = {"customer_id": str(customer)}
    head = {
        "Identity": identity,
        "Authorization": authorization,
        "Content-type": "application/json",
    }
    r = requests.post(url, headers=head, json=data)
    if r.status_code in [200, 201]:
        return r.json()
    raise HTTPException(status_code=500, detail="failed to create token")



def plaid_bond_test(account_id):
  return f"""
  <html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Plaid Quickstart Example</title>
    <link rel="stylesheet" href="https://threads.plaid.com/threads.css" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.2.3/jquery.min.js"></script>
    <script src="https://cdn.plaid.com/link/v2/stable/link-initialize.js"></script>
  </head>

  <body>
    <main class="main">
      <div class="grid">
        <div class="grid__column grid__column--is-twelve-columns">
          <div id="banner" class="everpresent-content">
            <h1 class="everpresent-content__heading">Plaid Quickstart</h1>
            <p id="intro" class="everpresent-content__subheading">
              An example application that outlines an end-to-end integration
              with Plaid
            </p>
          </div>

          <div id="container" class="initial-view">
            <p class="initial-view__description">
              Click the button below to open a list of Institutions. After you
              select one, you’ll be guided through an authentication process. If
              using the default Sandbox environment, use username
              <strong>user_good</strong> and password
              <strong>pass_good</strong>. Upon completion, a
              <code>public_token</code> will be passed back to the server and
              exchanged for <code>access_token</code>.
            </p>

            <button id="link-btn" class="button button--is-primary">
              Connect with Plaid
            </button>
            <div class="loading-indicator"></div>
          </div>
          <div id="display-plaid">

          </div>
      </main>
      </body>

      <script> 

      const new_elements= document.getElementById("display-plaid");
      function createPlaid( linkToken ) {{
            const handler = Plaid.create({{
              token: linkToken,
              onSuccess: make_post_request,
              onLoad: () => {{ console.log( "load" ); handler.open(); }},
              onExit: (err, metadata) => {{ console.log( "exit" ); }},
              onEvent: (eventName, metadata) => {{ console.log( `event: ${{eventName}}` );}},
              receivedRedirectUri: null,
            }});
      }}
      function make_post_request(public_token, metadata) {{
        console.log(public_token);
      }}
      function make_get_request() {{
          let resp = fetch( "/plaid/create_link_token")
            .then(response=>response.json())
            .then( data => {{
            console.log(data);
            createPlaid(data.link_token);
          }});

      }}
      
      const elements = document.getElementById("link-btn");
      elements.addEventListener('click', make_get_request, false);
      </script>
      </html>
  """

        # let resp = await fetch( "/accounts/{account_id}/create-link-token" );

        # new_elements.innerHTML= resp

# def plaid_bond_test(account_id):

# link-sandbox-f705d132-2475-4137-b935-6d320708ff62