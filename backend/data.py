import requests

def data(symbol):
    url = f"https://api.diadata.org/v1/quotation/{symbol.upper()}"

    try:
        response = requests.get(url, timeout=4)

        if response.status_code == 200:
           data = response.json()

           symbol = data.get("Symbol")
           price = data.get("Price")
           time = data.get("Time")

           return data
        elif response.status_code == 404:
            print(f"Error: The Symbol {symbol} is not available")
            return None
        else:
            print(f"Error")
            return None
    except requests.exceptions.RequestException as e:
        print("Connection Error")
        return None
