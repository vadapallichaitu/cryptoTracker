import requests # Install requests module first.

def candle_lit():
    candle_url = "https://public.coindcx.com/market_data/candles?pair=B-BTC_USDT&interval=1m" # Replace 'SNTBTC' with the desired market pair.

    candle_response = requests.get(candle_url)
    candle_data = candle_response.json()
    return candle_data

def ticker_lit():
    ticker_url = "https://api.coindcx.com/exchange/ticker"

    ticker_response = requests.get(ticker_url)
    ticker_data = ticker_response.json()
    return ticker_data

def market_lit():
    

    market_url = "https://api.coindcx.com/exchange/v1/markets_details"

    market_response = requests.get(market_url)
    market_data = market_response.json()
    return market_data

