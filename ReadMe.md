# mempool-Terminal: Verified Bitcoin wallet statements blazingly-fast

This document provides an overview and usage guidelines for mempool-Terminal, a Python program designed to fetch and analyze transactions associated with a specific Bitcoin address. The program utilizes various functionalities including fetching transactions and their details, calculating net amounts sent or received, and logging Bitcoin prices at transaction times. It also allows downloading transaction data as an Excel file for offline analysis.

## Acknowledgements

Mempool Open Source Project

## Features

- **Transaction Fetching:** Retrieve all transactions for a given Bitcoin address.
- **Transaction Analysis:** Calculate and display the net amount sent or received in each transaction, taking into account the amounts received as change.
- **Price Logging:** Log the Bitcoin price at the time of each transaction.
- **Excel Export:** Offer an option to download the transaction log and price data as an Excel file.

## Dependencies

The program relies on several external Python libraries:

- `requests`: For making HTTP requests to fetch transaction data.
- `datetime`: For handling dates and times, specifically for formatting transaction timestamps.
- `openpyxl`: For reading from and writing to Excel files.

Additionally, it utilizes custom modules:

- `prevout`: To search previous outputs (prevouts) for a given transaction.
- `mempool_requests`: To fetch transaction data and Bitcoin prices.
- `write_to_excel`: To write transaction data to an Excel file and log prices.

## Constants

- `BTC_DECIMAL`: A constant used to convert Satoshi to Bitcoin (1 BTC = 10^8 Satoshi).

## Main Functionality

1. **Input Bitcoin Address:** The program starts by prompting the user to enter a Bitcoin address for analysis.
2. **Fetch Transactions:** It retrieves all transactions associated with the provided Bitcoin address.
3. **Analyze Transactions:** For each transaction, the program:
   - Identifies inputs (vin) and outputs (vout).
   - Checks if the transaction includes the given Bitcoin address either as a sender or a receiver.
   - Calculates the net amount sent or received in the transaction.
   - Fetches the Bitcoin price at the time of the transaction.
4. **Display Transactions:** Displays each transaction's details including date, block height, transaction ID, amounts sent or received, and the Bitcoin price at the transaction time.
5. **Download Option:** After displaying all transactions, the program asks the user if they wish to download the transactions as an Excel file.
   - If yes, it proceeds to save the transaction data and price logs into an Excel file.
   - If no, it exits without downloading transactions.

### Usage

    To use mempool-Terminal, there are two primary methods: running the Python script directly after cloning the repository and installing dependencies, or downloading the executable app directly from the website. Follow the steps below for your preferred method:

    #### Option 1: Running the Python Script
    1. **Clone the Repository:** First, clone the repository to your local machine using Git:

       ```
       git clone https://github.com/madame-president/mempool-terminal.git
       ```

    2. **Install Dependencies:** Navigate to the cloned repository directory and install the required Python dependencies. Ensure you have Python and pip installed on your system, then run:

       ```
       pip install -r requirements.txt
       ```

    3. **Run the Script:** Once the dependencies are installed, you can run the script from the command line:

       ```
       python mempool-terminal.py
       ```

    #### Option 2: Downloading the Executable App

    1. **Download the App:** Visit the official website to download the executable app:

       ```
       https://mempool-terminal.com
       ```

    2. **Install the App:** Follow the installation instructions provided on the website or accompanying the downloaded file.

    3. **Run the App:** Once installed, open the application to start analyzing Bitcoin transactions without requiring manual setup or Python dependencies.


