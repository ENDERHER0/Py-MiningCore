import csv
from datetime import datetime
from BitcoinMiner.CryptoConnect import getTopCrypto


def update_crypto_csv(filename):
    # Sample top cryptocurrencies data for testing
    top_coins = getTopCrypto()

    # Get the current system time
    current_time = datetime.now().strftime("%Y-%m-%d %H.%M.%S")

    # Extract the names of cryptocurrencies
    crypto_names = [coin['name'] for coin in top_coins]

    # Check if the file exists and has data
    try:
        with open(filename, mode='r') as file:
            reader = csv.reader(file, delimiter=',')
            data = list(reader)
            if len(data) > 1:  # File has data
                last_entry = data[-1][2:]  # Get the last entry data (excluding index and date)
            else:
                last_entry = []  # No previous data
    except FileNotFoundError:  # File does not exist
        last_entry = []  # No previous data

    # Compare the last entry with the current data
    new_data_flag = False
    for coin in top_coins:
        if coin['name'] in crypto_names:
            coin_index = crypto_names.index(coin['name'])
            if last_entry and last_entry[coin_index] != str(coin['price']):
                new_data_flag = True
                break
            elif not last_entry:
                new_data_flag = True
                break

    if not new_data_flag:
        print("No new data to append. Previous data is the same as current data.")
        return

    # Open the CSV file in append mode
    with open(filename, mode='a', newline='') as file:
        # Create a CSV writer object
        writer = csv.writer(file, delimiter=',')

        # Write the names row if the file is empty
        if not last_entry:  # File is empty or no previous data
            # Insert the date tag
            first_row = ['Index', 'Date'] + crypto_names
            writer.writerow(first_row)

        # Write the date and prices in the next row
        entry_number = len(data) if data else 1
        price_row = [entry_number, current_time] + [coin['price'] if coin['name'] in crypto_names else '' for coin in
                                                    top_coins]
        writer.writerow(price_row)

    print(
        f"New data has been appended to the CSV file '{filename}' with the system upload time: {current_time} successfully.")


def read_crypto_csv(filename):
    data_array = []

    # Open the CSV file for reading
    with open(filename, mode='r', newline='') as file:
        # Create a CSV reader object
        reader = csv.reader(file, delimiter=',')

        # Read each row from the CSV file
        for row in reader:
            data_array.append(row)

    return data_array


# Usage example:
if __name__ == "__main__":
    filename = "StockData/stocks.csv"
    data_array = read_crypto_csv(filename)
    for row in data_array:
        print(row)

# Usage example:
if __name__ == "__main__":
    filename = "StockData/stocks.csv"
    update_crypto_csv(filename)
