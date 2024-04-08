import requests
import time
from datetime import datetime
from openpyxl import Workbook
from openpyxl import load_workbook
from prevout import search_prevouts
from mempool_requests import fetch_transactions, fetch_price
from write_to_excel import write_save_excel, price_log


BTC_DECIMAL = 10**8

def main():
    bitcoin_address = input("\u001b[1m\u001b[4m\u001b[40mPlease enter a Bitcoin address:\u001b[0m")
    transactions = fetch_transactions(bitcoin_address)
    price_data_list = []  # For price log


    # Compiles list of prevouts from tx inputs (tx['vin'])
    # vin represents an input to the current tx
    # prevout is the output from a previous tx that this input is spending
    
    if transactions:
        for tx in transactions:
            prevouts = [vin['prevout'] for vin in tx['vin'] if 'prevout' in vin]
            is_in_outputs = any(vout['scriptpubkey_address'] == bitcoin_address for vout in tx['vout'] if 'scriptpubkey_address' in vout)
            is_in_prevouts = search_prevouts(prevouts, bitcoin_address)

            if 'status' in tx and 'block_time' in tx['status'] and 'block_height' in tx['status']:
                tx_time = datetime.utcfromtimestamp(tx['status']['block_time']).strftime('%Y-%m-%d %H:%M:%S')
                block_height = tx['status']['block_height']
            else:
                tx_time = "Unconfirmed"
                block_height = "Unconfirmed"
            
            tx_id = tx['txid']

            # Fetch price for the tx
            if 'status' in tx and 'block_time' in tx['status']:
                price = fetch_price(timestamp=tx['status']['block_time'])
                price_data_list.append({'block_time': tx_time, 'price': price})
            
            if is_in_prevouts or is_in_outputs:
                sent_amount = sum(prevout['value'] for prevout in prevouts if prevout.get('scriptpubkey_address') == bitcoin_address) / BTC_DECIMAL
                received_amount = sum(vout['value'] for vout in tx['vout'] if vout.get('scriptpubkey_address') == bitcoin_address) / BTC_DECIMAL

                if is_in_prevouts and is_in_outputs:
                    net_amount = sent_amount - received_amount
                    if net_amount < 0:
                        net_amount_str = f"\u001b[1m{'{:.8f}'.format(net_amount)}\u001b[0m"
                    else:
                        net_amount_str = f"\u001b[33m{'{:.8f}'.format(net_amount)}\u001b[0m"
                    received_amount_str = f"{'{:.8f}'.format(received_amount)}"
                    
                    print(f"\u001b[44;1mDate:\u001b[0m \u001b[40;1m{tx_time}, \u001b[44;1mBlock Height:\u001b[0m \u001b[40;1m{block_height}, \u001b[44;1mTransaction ID:\u001b[0m \u001b[40;1m{tx_id}, \u001b[45;1m\u001b[1mSent Amount: {net_amount_str} \u001b[1m BTC, \u001b[7m\u001b[1mReceived Change: {received_amount_str} BTC\u001b[0m\u001b[1m")

                elif is_in_prevouts:
                    sent_amount_str = f"\u001b[1m\u001b[33m{'{:.8f}'.format(sent_amount)}\u001b[0m" if sent_amount >= 0 else f"\u001b[1m{'{:.8f}'.format(sent_amount)}\u001b[0m"
                    print(f"\u001b[44;1m\u001b[1mDate:\u001b[0m \u001b[40;1m{tx_time}, \u001b[44;1m\u001b[1mBlock Height:\u001b[0m \u001b[40;1m{block_height}, \u001b[44;1m\u001b[1mTransaction ID:\u001b[0m \u001b[40;1m{tx_id}, \u001b[43;1mSent Amount:\u001b[0m {sent_amount_str} \u001b[1m BTC")
                elif is_in_outputs:
                    received_amount_str = f"\u001b[1m\u001b[32m{'{:.8f}'.format(received_amount)}\u001b[0m"
                    print(f"\u001b[44;1m\u001b[1mDate:\u001b[0m \u001b[40;1m{tx_time}, \u001b[44;1m\u001b[1mBlock Height:\u001b[0m \u001b[40;1m{block_height}, \u001b[44;1m\u001b[1mTransaction ID:\u001b[0m \u001b[40;1m{tx_id}, \u001b[42;1mReceived Amount:\u001b[0m {received_amount_str} \u001b[1m BTC")

    # Total tx count displayed on terminal
        print(f"\u001b[45;1mTotal Transaction Count:\u001b[0m \u001b[45;1m{len(transactions)}\u001b[0m")

    # Prompt the user after displaying transactions
        user_choice = input("\u001b[41;1m\u001b[1m\u001b[4mDo you want to download the displayed transactions as an Excel file? (yes/no):\u001b[0m").lower()
        if user_choice == "yes":
           # write_save_excel returns the filename
            excel_file_path = write_save_excel(transactions, bitcoin_address)
            # Pass the filename to price_log
            price_log(excel_file_path, price_data_list)
        else:
            print("Exiting without downloading transactions.")

    else:
        print("No transactions found for this address.")



if __name__ == "__main__":
    main()