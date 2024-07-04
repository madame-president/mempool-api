import requests
import time
import pandas as pd
import sys
from tabulate import tabulate
from datetime import datetime, timezone
from prevouts import search_prevouts
from getData import get_transactions, get_price

bitcoin_power = 10**8

def main():
    user_address = input("Please enter a Bitcoin Address: ")
    fetched_transactions = get_transactions(user_address)
    price_log = []
    table_data = []

    if fetched_transactions:
        for tx in fetched_transactions:

            sent_amount = '0'
            received_amount = '0'

            prevouts = [vin['prevout'] for vin in tx['vin'] if 'prevout' in vin]
            found_in_outputs = any(vout['scriptpubkey_address'] == user_address for vout in tx['vout'] if 'scriptpubkey_address' in vout)
            found_in_prevouts = search_prevouts(prevouts, user_address)

            # If all 3 conditions == TRUE, then the transaction has been confirmed.
            if 'status' in tx and 'block_time' in tx['status'] and 'block_height' in tx['status']:
                server_time = datetime.fromtimestamp(tx['status']['block_time'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                block_height = tx['status']['block_height']
            else:
                server_time = "Unconfirmed"
                block_height = "Unconfirmed"

            tx_id = tx['txid']

            # Get price
            if 'status'  in tx and 'block_time' in tx['status']:
                price = get_price(timestamp=tx['status']['block_time'])
                price_log.append({'block_time': server_time, 'price': price})

            if found_in_prevouts or found_in_outputs:
                sent_amount = sum(prevout['value'] for prevout in prevouts if prevout.get('scriptpubkey_address') == user_address) / bitcoin_power
                received_amount = sum(vout['value'] for vout in tx['vout'] if vout.get('scriptpubkey_address') == user_address) / bitcoin_power
                    
            # Display data in table format
            table_data.append({
                "Server Time": server_time,
                "Block": block_height,
                "Transaction ID": tx_id,
                "Sent": sent_amount,
                "Received": received_amount,
                "BTC/USD": "{:,.2f}".format(price)
            })

            # Character limits
            max_width = 64
            for entry in table_data:
                entry['Transaction ID'] = entry['Transaction ID'][:20] + '...'
                for key in entry:
                    if key!= 'Transaction ID':
                        entry[key] = str(entry[key])[:max_width]

        # Convert list to dataframe
        table_df = pd.DataFrame(table_data)

        # Adjust dataframe index
        table_df.index = range(1, len(table_df) + 1)

        transactions_table = tabulate(table_df, headers='keys', tablefmt='fancy_grid', colalign=('left', 'right', 'center'))
        print(transactions_table)

        print(f"Total Transaction Count: {len(fetched_transactions)}")
    else:
        print("No transactions found for this address.")
        pass

if __name__ == "__main__":
    while True:
        main()
        # Get user input
        loop_input = input("Press Enter to run the program again or type 'exit' and press Enter to quit: ")
        if loop_input.lower() == 'exit':
            sys.exit()  # Exit loop