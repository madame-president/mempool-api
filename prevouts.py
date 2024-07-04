# Checks if user_address is found in tx inputs' prevouts

def search_prevouts(prevout, user_address):
    return any(
        prevout['scriptpubkey_address'] == user_address
        for prevout in prevout
        if 'scriptpubkey_address' in prevout
    )
    pass