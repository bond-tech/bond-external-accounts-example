
from app.constants import (
    identity , authorization , bond_host
)

def create_token(customer):
    url = "https://api.bond.tech/api/v0/auth/key/temporary"
    data = {"customer_id":customer}
    head = {
        'Identity': identity , 
        'Authorization': authorization , 
        'Content-type': 'application/json' ,
    }
    r = requests.post(url, headers=head, json=data)
    if r.status_code in [200,201]: 
        return r.json()
    raise HTTPException(status_code=500, detail="failed to create token")

def card_view_page(customer, card):
    return f"""<html>
<head>
<script type="text/javascript" src='https://cdn.bond.tech/sdk/cards/v1/bond-sdk-cards.js'></script>
</head>
<body>

<div class="field">
  Card Number
  <div id="num" class="card-field"></div>
</div>
<div class="field">
  Expiration Date
  <div id="exp" class="card-field"></div>
</div>
<div class="field">
  CVV2
  <div id="cvv" class="card-field"></div>
</div>

<script>
const cards = new BondCards({{ live: true }});

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
      }})
      .then((data) => {{ console.log("ok?"); }})
      .catch((error) => {{ console.log("error?"); }});

}} );

</script>
</body>
</html>
"""
