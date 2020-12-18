
def format_page(customer_id, card_id):
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

fetch( "/token/{customer_id}" )
  .then( response => response.json() )
  .then( data => {{
    console.log( data );
    cards
      .show({{
        cardId: "{card_id}",
        identity: data.Identity,
        authorization: data.Authorization,
        field: "number",
        htmlSelector: "#num",
      }})
      .then((data) => {{ console.log("ok?"); }})
      .catch((error) => {{ console.log("error?"); }});

    cards
      .show({{
        cardId: "{card_id}",
        identity: data.Identity,
        authorization: data.Authorization,
        field: "expiry",
        htmlSelector: "#exp",
      }})
      .then((data) => {{ console.log("ok?"); }})
      .catch((error) => {{ console.log("error?"); }});

    cards
      .show({{
        cardId: "{card_id}",
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
