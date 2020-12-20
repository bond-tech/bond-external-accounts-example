
import requests

from fastapi import HTTPException

from app.constants import (
    identity , authorization , bond_host , sdk_docs , api_docs
)

def create_token(customer):
    url = "https://api.bond.tech/api/v0/auth/key/temporary"
    data = {"customer_id":str(customer)}
    head = {
        'Identity': identity , 
        'Authorization': authorization , 
        'Content-type': 'application/json' ,
    }
    r = requests.post(url, headers=head, json=data)
    if r.status_code in [200,201]: 
        return r.json()
    raise HTTPException(status_code=500, detail="failed to create token")

def card_view_page(customer, card, live=False):
    return f"""<html>
<head>
<script type="text/javascript" src='https://cdn.bond.tech/sdk/cards/v1/bond-sdk-cards.js'></script>
<script src="https://kit.fontawesome.com/bf83d14d06.js" crossorigin="anonymous"></script>
<link rel="stylesheet" href="/static/styles.css">
</head>
<body>

  <main>
    <center>
    <div class="container">

      <div class="field width100">
        Bond Card Id:
        <div id="card-id" class="card-field display">{card}</div>
      </div>
      <div class="field width100 footer-font">
        <a href="{sdk_docs}" target="_blank" rel="noopener noreferrer">
          Bond Cards SDK documentation
        </a>
      </div>
      <div class="field width100 footer-font">
        <a href="{api_docs}" target="_blank" rel="noopener noreferrer">
          Bond Studio API documentation
        </a>
      </div>

      <br/><hr/><br/>

      <div class="field width100">
        Card Number:
        <div id="num" class="card-field"></div>
      </div>
      <div class="field row">
        <div class="field width40">
          Expiration Date: 
          <div id="exp" class="card-field"></div>
        </div>
        <div class="field width40">
          CVV2: 
          <div id="cvv" class="card-field"></div>
        </div>
      </div>

      <br/><hr/>

      <div class="field row">
        <div class="field width30">
          Current PIN: 
          <div id="view-pin" class="card-field"></div>
        </div>
        <div class="field width30"></div>
        <div class="field width20 icon">
          <i class="fas fa-eye fa-2x"></i>
        </div>
      </div>

      <br/><hr/>

      <div class="field row">
        <div class="field width30">
          Current PIN: 
          <div id="current-pin" class="card-field"></div>
        </div>
        <div class="field width30">
          New PIN: 
          <div id="new-pin" class="card-field"></div>
        </div>
        <div class="field width20 icon">
            <i class="fas fa-arrow-circle-right fa-2x"></i>
        </div>
      </div>

      <br/><hr/>

      <div class="field row">
        <div class="field width30">
          Reset PIN: 
          <div id="rest-pin" class="card-field"></div>
        </div>
        <div class="field width30"></div>
        <div class="field width20 icon">
            <i class="fas fa-arrow-circle-right fa-2x"></i>
        </div>
      </div>

    </div>
    </center>
  </main>

<script>
const cards = new BondCards({{ live: {"true" if live else "false"} }});

const css = {{ 
  fontFamily: 'Sans-Serif',
  fontSize: '1.15em',
  color: "rgb(96,107,243)" ,
}};

fetch( "/token/{customer}" )
  .then( response => response.json() )
  .then( data => {{
    console.log( data );
    cards
      .show({{
        cardId: "{card}",
        identity: data.Identity,
        authorization: data.Authorization,
        field: "number",
        htmlSelector: "#num",
        css: css,
      }})
      .then((data) => {{ console.log("ok?"); }})
      .catch((error) => {{ console.log("error?"); }});

    cards
      .show({{
        cardId: "{card}",
        identity: data.Identity,
        authorization: data.Authorization,
        field: "expiry",
        htmlSelector: "#exp",
        css: css,
      }})
      .then((data) => {{ console.log("ok?"); }})
      .catch((error) => {{ console.log("error?"); }});

    cards
      .show({{
        cardId: "{card}",
        identity: data.Identity,
        authorization: data.Authorization,
        field: "cvv",
        htmlSelector: "#cvv",
        css: css,
      }})
      .then((data) => {{ console.log("ok?"); }})
      .catch((error) => {{ console.log("error?"); }});

}} );

</script>
</body>
</html>
"""
