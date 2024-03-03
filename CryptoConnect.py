import requests


def getTop10Coins():
    url = 'https://api.coingecko.com/api/v3/coins/markets'
    params = {
        'vs_currency': 'usd',
        'order': 'market_cap_desc',
        'per_page': 10,
        'page': 1,
        'sparkline': 'false'
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        # Extracting only the required information (name and current price) for each coin
        top_coins = [{"name": coin["name"], "current_price": coin["current_price"]} for coin in data]
        return top_coins
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None


def getTopCrypto():
    topCoins = getTop10Coins()
    # topCoins = None
    if topCoins is not None:
        currentTopCoins = []
        for coin in topCoins:
            coinName = coin['name']
            coinPrice = coin['current_price']
            currentTopCoins.append({"name": coinName, "price": coinPrice})
        print("Coins Called")
        return currentTopCoins
    else:
        missingResponse = [{'name': "missing"}], [{'price': "0.00"}]
        missingCoin = []
        for i in range(9):
            coinName = missingResponse[0][0]['name']
            coinPrice = missingResponse[1][0]['price']

            missingCoin.append({"name": coinName, "price": coinPrice})
        print("Coins not callable")
        return missingCoin

# print(getTopCrypto())
