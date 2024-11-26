# Mempool API

## External and internal packages and modules

1. **requests:** for sending HTTP requests to servers.

2. **time:** provides time-related functions. Used in our program to avoid request limitations.

3. **pandas:** provides data manipulation structures. Used in our program to organize our data into a *DataFrame*.

4. **sys:** provides access to system functions. Used in our program to exit loops and use of ease.

5. **tabulate:** formats data as plain text tables to display in the terminal.

6. **datetime** and **timezone:** *datetime* provides date and time functions. *timezone* converts the block times into readable UTC dates and times.

# Main file: run

1. We start by defining a constant ```sats_to_btc``` to convert satoshis to Bitcoin. This constant is later referenced.

2. ```main()``` is the primary function of our program. We start by creating a variable that takes our input. We want the program to prompt us to enter our Bitcoin address.

3. We will now call the function we previously created ```get_transactions``` to fetch the transactions from the address we will input ```user_address``` and store our fetched data in the variable ```fetched_transactions```.

4. Let's also add two empty lists: ```price_log``` and ```table_data``` to store the price data of our Bitcoin transactions and relevant transaction details, such as timestamps, amounts, and txids.

5. If ```fetched_transactions``` contains data, let's have the program iterate over each transaction. Let's also set ```sent_amount``` and ```received_amount``` as strings to '0'. I found it was easier for the program to process the amounts as strings. They will be updated later in the loop, based on the transaction's inputs (vin) and outputs (vout).

6. Let's extract the previous transaction output, from each transaction input (```vin```) in the current transaction (```tx```). For each input that contains a prevout, the prevout is added to the list of ```prevouts```.

7. Now let's focus on the transaction outputs (```vout```). We need to check if our address is found in any of the outputs of the transaction (```tx['vout']```). Creating this list will help us iterate through each output, and check if our address matches the ```scriptpubkey_address```. If our address is found in the outputs of the transaction, it indicates we *received* Bitcoin.

8. If our address is found in the ```prevouts``` of the transaction, we will call the ```search_prevouts``` function. This function will iterate over all the prevouts and check if our address matches the ```scriptpubkey_adddress``` in any of the previous outputs. ```found_in_prevouts``` will be ```True``` if the address we entered is found, and can classify the transaction as *sent*.

9. Let's now extract the relevant transaction details we need for our report. Let's check if the transaction (```tx```) has a ```status``` field and if that contains both ```block_time``` and ```block_height```.

10. After we extract the confirmation time and block height, let's convert the ```block_time``` into a readable datetime format (UNIX to YYYY/MM/DD H:M:S).

11. If the transaction does not have a status, it means the transaction is unconfirmed.

12. We will also store the txid  (Transaction ID) from the ```tx``` object to a new variable named ```tx_id```.

13. Let's add a few tasks related to the price of Bitcoin at the time of transaction and calculate the amounts sent or received. If the ```status``` field contains a ```block_time```, we will call the ```get_price``` function, passing the timestamp of the transaction to fetch the price of Bitcoin at that time.

14. ```get_price``` queries historical price data and returns the price of Bitcoin in our specified currency at that particular timestamp. The prices are appended to the ```price_log``` list, which also stores the price along with the formatted ```server_time```.

15. Next, we define our transaction amount calculation. The calculations are done after classifying each transaction as *sent* or *received* by converting from sats to BTC using the ```sats_to_btc``` factor.

16. Let's format and display the transaction data in a table, and then print that table into the terminal. We will append each transaction to our ```table_data```. 

17. We will format the amounts of Bitcoin transacted to 8 decimal places and the price of Bitcoin in USD at the time of transaction formatted to 2 decimal places.

18. Let's now use pandas to convert our data into a Pandas DataFrame. This makes it easier to manipulate data because it takes our previous list, and converts the data in a tabular format.

19. ```table_df.index = range(1, len(table_df) + 1)``` sets the index of the DataFrame to start at 1 and go up to the number of transactions, so the rows will be numbered starting from 1.

20. We then use the ```tabulate``` function to convert the DataFrame into a human-readable format. I will specify to use the column names as the headers and style the table's borders and cell formatting.

21. Let's print the table onto our terminal and display the total number of transactions our Bitcoin address has.

22. We want to ensure the program runs continuously, allowing us to run the main function multiple times or quit the program. While ```True```, we want the program to keep running until explicitly told to stop. ```loop_input``` stores our response, which can either be the Enter key (to run the program again) or the word ```'exit'``` (to quit the program).


# Module: getData (get_transactions)

1. Let's start by importing ```requests``` to make an HTTP request to *mempool.space* servers.

2. We will now create a function named ```get_transactions``` tasked with retrieving our Bitcoin transaction data. This function will take an input named ```user_address```, which the program will prompt us to enter later on.

3. Now, let's create an empty list ```fetched_transactions = []``` to store our transaction data.

4. We grab our ```address_url``` from *mempool.space documentation* and create a variable ```endpoint``` that appends our ```user_address``` and the path ```/txs``` to the base URL.

5. According to their documentation, we are responsible for handling pagination. Since there is no prior transaction to reference, we will initialize the variable ```after_txid``` to ```None```.

6. When ```after_txid``` has subsequent requests, we append the query parameter to the ```endpoint``` URL.

7. Let's make the API request. The loop will continue if the status code equals 200.

8. Because the data returned is in JSON format, we need to convert it into an object ```paginated_transactions```.

9. If ```paginated_transactions``` returns empty, there are no more transactions available and the loop will break.

10. If it's not empty, the program will continue paginating transactions.

11. We can now add our paginated transactions to our ```fetched_transactions``` list. Let's also sort the transactions from newest to oldest and update ```after_txid``` with the last confirmed txid.

12. If the API request fails to receive status code 200, we want the program to let us know what happened. We will make the program print out a message containing the status code received and add a ```break``` to avoid further processing.

13. If all goes as planned, the program will ```return fetched_transactions```.

# Module: getData (get_price)

1. Let's create a function to fetch the historical price of Bitcoin in a specified fiat currency at a given timestamp ```get_price```. This function will take in two parameters: ```currency``` and ```timestamp```. I set my currency to USD because BTC/USD is the largest market and the timestamp is defaulted to ```None```.

2. Just like before, we need to construct a URL to make the request ```historical_price_url```to *mempool.space*, including our query paramenters.

3. After we make the request, we want to make sure the ```response``` fetched the historical price data from the servers, so we check one more time for status code 200.

4. Let's take the JSON format response and convert it into a dictionary ```data```. We want to check if the ```prices``` key contains data. If ```prices``` contains data, it will return the price for the requested currency. If ```prices``` is empty, the function will return ```None```.

5. If the request fails to produce status code 200, the function will also return ```None```.

# Module: prevouts (search_prevouts)

1. ```search_prevouts``` will determine if the Bitcoin address we input (```user_address```) exists in the ```prevout``` list. We will take both as parameters and create a list of dictionaries, where each dictionary will represent a previous output from a Bitcoin transaction and search for our address in the list.

2. We only care about processing dictionaries that match the address we entered. It returns ```True``` if at least one item in prevout matches our address and return ```False``` if no items match.

3. If one or more ```prevouts``` match our Bitcoin address, it means that we previously owned these Bitcoin outputs, which are now being *spent* in the transaction. It indicates that the transaction involves *sending* Bitcoin to another recipient.

4. A transaction is *received* if our Bitcoin address is found in the outputs (vout) because is where new Bitcoin amounts are *"credited"*.

5. If our Bitcoin address is found in both ```prevouts``` and ```vout```, the transaction may involve:

    - Sending Bitcoin to oneself.
    - Sending Bitcoin to another address while receiving change back.


# Module X: Addressing common issues

1. Classifying transactions as *sent* or *received*.

2. Understanding which key values are relevant to your Bitcoin address and transactions.




