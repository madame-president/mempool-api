import requests
import time
import pandas as pd
import sys
from tabulate import tabulate
from datetime import datetime, timezone
from openpyxl import Workbook
from getData import get_transactions, get_price
from prevouts import search_prevouts

sats_to_btc = 10**8

 # Start main function
def main():
    user_address = input("Please enter a Bitcoin Address: ")
    transactions = get_transactions(user_address)
    price_log = []
    table_data = []

     # Start 'main' loop
    if transactions:
        for tx in transactions:
            tx_id = tx['txid']

             # Get transaction status
            if 'status' in tx and 'block_time' in tx['status'] and 'block_height' in tx['status']:
                server_time = datetime.fromtimestamp(tx['status']['block_time'], timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
                block_height = tx['status']['block_height']
            else:
                server_time = "Unconfirmed"
                block_height = "Unconfirmed"

             # Get price
            if 'status' in tx and 'block_time' in tx['status']:
                price = get_price(timestamp=tx['status']['block_time'])
                price_log.append({'block_time': server_time, 'price': price})

             # Classify transaction type
            sent_amount = '0'
            received_amount = '0'
            prevouts = [vin['prevout'] for vin in tx['vin'] if 'prevout' in vin]
            found_in_outputs = any(vout['scriptpubkey_address'] == user_address for vout in tx['vout'] if 'scriptpubkey_address' in vout)
            found_in_prevouts = search_prevouts(prevouts, user_address)

            if found_in_prevouts or found_in_outputs:
                sent_amount = sum(prevout['value'] for prevout in prevouts if prevout.get('scriptpubkey_address') == user_address) / sats_to_btc
                received_amount = sum(vout['value'] for vout in tx['vout'] if vout.get('scriptpubkey_address') == user_address) / sats_to_btc

             # Display data in table format
            table_data.append({
                "Server Time": server_time,
                "Block": block_height,
                "Transaction ID": tx_id,
                "Sent": f"{sent_amount:.8f}",
                "Received": f"{received_amount:.8f}",
                "BTC/USD": "{:,.2f}".format(price)
            })

        table_df = pd.DataFrame(table_data)
        table_df.index = range(1, len(table_df) + 1)
        transactions_table = tabulate(table_df, headers='keys', tablefmt='fancy_grid', colalign=('left', 'right', 'center'))
        print(transactions_table)
        print(f"Total Transaction Count: {len(transactions)}")

         # Prompt to download the dataframe as an Excel file
        download_input = input("Download .xlsx file? (y/n): ")
        if download_input.lower() == 'y':
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            filename = f"{user_address}_{timestamp}_report.xlsx"
            table_df.to_excel(filename, index=False)
            print(f"Saved the report to {filename}")
    else:
        print("No transactions found for this address.") # End 'main' loop

if __name__ == "__main__":
    while True:
        main()
        loop_input = input("Press Enter to run the program again or type 'exit' and press Enter to quit: ")
        if loop_input.lower() == 'exit':
            sys.exit()  # Exit program
