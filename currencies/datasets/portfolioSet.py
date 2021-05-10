import hmac
import hashlib
import base64
import json
import time
import requests
import hmac
import plotly.graph_objects as go
import pandas as pd
import pandasql as ps
from ..models import KeyFormModel
# Enter your API Key and Secret here. If you don't have one, you can generate it from the website.
def Total_holdings(primary_key,secret_key):
    if(KeyFormModel):
        key = primary_key
        secret = secret_key
        
        # python3
        secret_bytes = bytes(secret, encoding='utf-8')
        # python2
        #secret_bytes = bytes(secret)

        # Generating a timestamp.
        timeStamp = int(round(time.time() * 1000))

        body = {
            "timestamp": timeStamp
        }

        json_body = json.dumps(body, separators = (',', ':'))

        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

        url = "https://api.coindcx.com/exchange/v1/users/balances"

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }

        response = requests.post(url, data = json_body, headers = headers)
        data = response.json();
        curr_list=[]
        for i in data:
            if(i["balance"]!='0.0'):
                curr_list.append(i["currency"])



        # Enter your API Key and Secret here. If you don't have one, you can generate it from the website.


        # python3
        secret_bytes = bytes(secret, encoding='utf-8')


        # Generating a timestamp
        timeStamp = int(round(time.time() * 1000))

        body = {
            "timestamp": timeStamp
        }

        json_body = json.dumps(body, separators = (',', ':'))

        signature = hmac.new(secret_bytes, json_body.encode(), hashlib.sha256).hexdigest()

        url = "https://api.coindcx.com/exchange/v1/users/balances"

        headers = {
            'Content-Type': 'application/json',
            'X-AUTH-APIKEY': key,
            'X-AUTH-SIGNATURE': signature
        }
        currency = []
        balance = []
        locked_balance=[]
        response = requests.post(url, data = json_body, headers = headers)
        data = response.json();
        for curr in data:
            if(curr['balance'] != '0.0' and curr['currency'] not in ['ALGO','INR']):
                balance.append(curr['balance'])
                currency.append(curr['currency']+'INR')
                locked_balance.append(curr['locked_balance'])
                


        PORTFOLIO =pd.DataFrame({'CURRENCY':currency,'BALANCE':balance,'LOCKED_BALANCE':locked_balance})


        url = "https://api.coindcx.com/exchange/ticker"

        response = requests.get(url)
        data = response.json()
        market = []
        last_price = []

        for currdetail in data:
            if(currdetail['market'] in currency):
                market.append(currdetail['market'])
                last_price.append(currdetail['last_price'])
        market_ticker = go.Figure(data=[go.Table(header=dict(values=['market', 'last_price']),
                        cells=dict(values=[market, last_price]))
                            ])



        LAST_PRICE_TABLE = pd.DataFrame({'MARKET':market,'LAST_PRICE':last_price})



        TOTAL=ps.sqldf('''
                        SELECT A.MARKET,
                            A.LAST_PRICE,
                            B.BALANCE as ACTIVE_BALANCE,
                            B.LOCKED_BALANCE,
                            (B.BALANCE+LOCKED_BALANCE) as TOTAL_BALANCE,
                            (LAST_PRICE*(B.BALANCE+LOCKED_BALANCE)) as TOTAL_HOLDING
                            FROM LAST_PRICE_TABLE A JOIN PORTFOLIO B ON A.MARKET=B.CURRENCY'''
                            )
        PIE = ps.sqldf(''' SELECT MARKET,TOTAL_HOLDING FROM TOTAL''')
        dfpair = {'total_df':TOTAL,'pie_df':PIE}
        return(dfpair)
