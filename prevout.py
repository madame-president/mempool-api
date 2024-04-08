# Checks if bitcoin_address is found in the tx inputs' prevouts.

def search_prevouts(prevouts, bitcoin_address):
    return any(
      prevout['scriptpubkey_address'] == bitcoin_address 
      for prevout in prevouts 
      if 'scriptpubkey_address' in prevout
    )
    pass