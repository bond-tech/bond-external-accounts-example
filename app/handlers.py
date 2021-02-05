import requests

from fastapi import HTTPException

from app.constants import *

def create_access_token(account_id, payload):
  public_token = payload["public_token"]
  metadata = payload["metadata"]
  linked_account_id = payload['linked_account_id']
  # change this once only 1 account is linked
  verification_status = metadata["accounts"][0].get("verification_status", "instant_verified") 
  external_account_id = metadata["accounts"][0]["id"]

  print(external_account_id)

  if account_id == "plaid":
      endpoint = "/item/public_token/exchange"
      url = plaid_host + endpoint

      headers = {
      "Content-type": "application/json",
      }

      payload = {
        "client_id": PLAID_CLIENT_ID,
        "secret": PLAID_SECRET,
        "public_token": public_token
      }

      r = requests.post(url=url, headers = headers, json=payload)
      return r.json()

  else:
      # Bond
      endpoint = f"/api/v0/accounts/{account_id}/external_accounts/plaid"
      url = bond_host + endpoint

      headers = {
          "Identity": identity,
          "Authorization": authorization,
          "Content-type": "application/json",
      }

      payload = {
        "public_token": public_token,
        "linked_account_id": linked_account_id,
        "external_account_id": external_account_id,
        "status": verification_status
      }
      # payload = {
      #   "public_token": "public-sandbox-98ed91d9-7794-49e2-a397-279734e597ae",
      #   "linked_account_id": "f897b0ac-f5aa-4802-ae1d-fd6b32f0ade9",
      #   "external_account_id": "nZyRwRlwo9CnjpGxjb4qcRMgmaePPBF8ZJgD3",
      #   "status": "pending_automatic_verification"
      # }

      r = requests.post(url=url, headers = headers, json=payload)
      return r.json()


def create_link_token(account_id):
  if account_id == "plaid":
    endpoint = "/link/token/create"
    url = plaid_host + endpoint

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

  else:
      # Bond
      endpoint = f"/api/v0/accounts/{account_id}/external_accounts/plaid"
      url = bond_host + endpoint

      headers = {
          "Identity": identity,
          "Authorization": authorization,
          "Content-type": "application/json",
      }
      
      r = requests.get(url=url, headers = headers)
      return r.json()


# createLinkToken -> initializePlaidLink -> createAccessToken
def plaid_bond_test(account_id):
  return f"""
  <html lang="en">
  <head>
    <meta charset="UTF-8" />
    <title>Plaid-Bond Quickstart Example</title>
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
            <h1 class="everpresent-content__heading">Plaid-Bond Quickstart</h1>
            <p id="intro" class="everpresent-content__subheading">
              An example application that outlines an end-to-end integration
              with Plaid and Bond
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

      function initializePlaidLink( data ) {{
        const handler = Plaid.create({{
          token: data.link_token,
          onSuccess: (public_token, metadata) => createAccessToken(public_token, metadata, data),
          onLoad: () => {{ console.log( "load" ); handler.open(); }},
          onExit: (err, metadata) => {{ console.log( "exit" ); }},
          onEvent: (eventName, metadata) => {{ console.log( `event: ${{eventName}}` );}},
          receivedRedirectUri: null,
        }});
      }}

      function createAccessToken(public_token, metadata, data) {{
        console.log("Successfully initialized plaid link object");
        console.log("Exchanging", public_token, "to get an access_token");
        let resp = fetch( "/plaid/create_access_token/{account_id}", {{
          method : "POST",
          headers: {{
            "Accept": "application/json",
            "Content-Type": "application/json"
          }},
          body: JSON.stringify({{
            "public_token": public_token, 
            "metadata": metadata,
            "linked_account_id": data.linked_account_id
            }})
        }}
        )
          .then(response=>response.json())
          .then( data => {{
          console.log(data);
        }});
      }}

      function createLinkToken() {{
          let resp = fetch( "/plaid/create_link_token/{account_id}")
            .then(response=>response.json())
            .then( data => {{
            console.log("link_token created.", data);
            initializePlaidLink(data);
          }});
      }}
      
      const elements = document.getElementById("link-btn");
      elements.addEventListener('click', createLinkToken, false);
      </script>
      </html>
  """