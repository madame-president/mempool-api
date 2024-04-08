import requests


def fetch_transactions(bitcoin_address):
  transactions = []
  base_url = "https://mempool.space/api/address/"
  endpoint = f"{base_url}{bitcoin_address}/txs"

  after_txid = None  # To handle better pagination = None {first request}
  while True:
    # If after_txid is set, append it to the endpoint URL
    # to fetch the next page of confirmed transactions
    url = f"{endpoint}?after_txid={after_txid}" if after_txid else endpoint

    response = requests.get(url)
    if response.status_code == 200:
      new_transactions = response.json()
      if not new_transactions:
        break  # Exit loop if no more txs are returned

      transactions.extend(new_transactions)
      # Updates after_txid for the next page with the last confirmed tx's txid
      # Sorts newest to oldest
      after_txid = new_transactions[-1]['txid']
    else:
      print(f"Failed to fetch transactions,"
            f" status code: {response.status_code}")
      break

  return transactions


def fetch_price(currency='USD', timestamp=None):
  # Using the Mempool API endpoint for historical prices.
  api_url = f"https://mempool.space/api/v1/historical-price?currency={currency}&timestamp={timestamp}"
  response = requests.get(api_url)
  if response.status_code == 200:
    data = response.json()
    if data['prices']:
      price_info = data['prices'][0]
      # Return the price in the requested currency.
      return price_info[currency]
    else:
      return None
  else:
    return None