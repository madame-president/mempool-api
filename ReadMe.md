# "Mempool" Terminal: verified Bitcoin wallet statements blazingly-fast

This document provides an overview and usage guidelines for Mempool Terminal.

## Acknowledgements

Thank you [Mempool.space](https://mempool.space) for building the robust APIs that made this possible.

## Features

- **Fetch Transactions:** Get all transactions for a given Bitcoin address.
- **Table Display:** local user-friendly display.
- **Price Logging:** Log the Bitcoin price at the time of each transaction
- **Export to Excel:** Coming Soon!

## Dependencies

Mempool Terminal relies on several Python Libraries:

- `requests`: For making HTTP requests
- `datetime`: For handling dates and times
- `tabulate`: For easy table display
- `openpyxl`: For reading and writing .xlsx files

Other modules:

- `prevouts`: To search previous outputs for a given transaction
- `getData`: To fetch transaction data and Bitcoin prices

## Constants

- `bitcoin_power`: Used to convert sats to Bitcoin (1 BTC = 10^8 Satoshi)

## Usage

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
       python run.py
       ```

#### Option 2: Downloading the Executable App

   1. **Download the App:** Visit the official website to download the executable app:

       ```
       https://mempool-terminal.com
       ```

   2. **Install the App:** Follow the installation instructions provided on the website or accompanying the downloaded file.

   3. **Run the App:** Once installed, open the application to start analyzing Bitcoin transactions without requiring manual setup or Python dependencies.
