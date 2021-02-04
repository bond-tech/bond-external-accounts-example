import requests

from fastapi import HTTPException

from app.constants import *

def create_access_token(account_id, payload):
  # return {"Hello" : "World"}
  public_token = payload["public_token"]
  metadata = payload["metadata"]
  if account_id == "plaid":
      url = f"https://sandbox.plaid.com/item/public_token/exchange"
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
      url = f"https://api.dev.bond.tech/api/v0/accounts/{account_id}/external_accounts/plaid"
      headers = {
          "Identity": identity,
          "Authorization": authorization,
          "Content-type": "application/json",
      }
      payload = {
        "public_token": public_token,
        "accounts": metadata.accounts,
        "institution": metadata.institution,
        "link_session_id": metadata.link_sess
        
        }
      r = requests.post(url=url, headers = headers, json=payload)
      return r.json()


def create_link_token(account_id):
  if account_id == "plaid":

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

  else:
      # Bond
      url = f"https://api.dev.bond.tech/api/v0/accounts/{account_id}/external_accounts/plaid"
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

      function initializePlaidLink( linkToken ) {{
            const handler = Plaid.create({{
              token: linkToken,
              onSuccess: createAccessToken,
              onLoad: () => {{ console.log( "load" ); handler.open(); }},
              onExit: (err, metadata) => {{ console.log( "exit" ); }},
              onEvent: (eventName, metadata) => {{ console.log( `event: ${{eventName}}` );}},
              receivedRedirectUri: null,
            }});
      }}

        function createAccessToken(public_token, metadata) {{
        console.log(public_token);
        console.log("metadata",metadata);
        let resp = fetch( "/plaid/create_access_token/{account_id}", {{
          method : "POST",
          headers: {{
            "Accept": "application/json",
            "Content-Type": "application/json"
          }},
          body: JSON.stringify({{
            "public_token": public_token, 
            "metadata": metadata
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
            console.log(data);
            initializePlaidLink(data.link_token);
          }});
      }}
      
      const elements = document.getElementById("link-btn");
      elements.addEventListener('click', createLinkToken, false);
      </script>
      </html>
  """



      # function createAccessToken(public_token, metadata) {{
      #   console.log(public_token);
      #   let resp = fetch( "/plaid/create_access_token/{account_id}/public_token")
      #     .then(response=>response.json())
      #     .then( data => {{
      #     console.log(data);
      #   }});
      # }}




  #POST ACCESS TOKEN

      #   function createAccessToken(public_token, metadata) {{
      #   console.log(public_token);
      #   let resp = fetch( "/plaid/create_access_token/{account_id}", {{
      #     method : "POST",
      #     headers: {{
      #       "Accept": "application/json",
      #       "Content-Type": "application/json"
      #     }},
      #     body: JSON.stringify({{"public_token": public_token}})
      #   }}
      #   )
      #     .then(response=>response.json())
      #     .then( data => {{
      #     console.log(data);
      #   }});
      # }}