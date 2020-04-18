#TODO
#1) Get cryptocurrencies from comacap api
#2) Create telegram bot with botfather
#3) create a flask app and handle requests from telegram
#4) Combine comacap parser and telegram bot
#5) Deploy to pythonanywhere and install flask-SSLify to solve SSL certificate issue

from tokens import cmc_token
import requests
import json
from flask import Flask
from flask import request
from flask_sslify import SSLify
from flask import Response
import re

#Telegram 
token = '948482927:AAEckZdqwfyrxcazcQLGAmFyXf3GNctg450'

#Flask app
app = Flask(__name__)
sslify =SSLify(app)

#Writting response data into Json and prettyfy
def write_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent = 4, ensure_ascii=False)
    
#Sending requests to CoinMarketCap and getting response on params
def getComaCap_Data(crypto):
    
    #vars
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    #?symbol=BTC,ETH,XRP,BCH,EOS,LTC,XLM&convert=BTC,ETH,EUR
    params = {'symbol' : crypto, 'convert' : 'INR'}
    headers = {'X-CMC_PRO_API_KEY' : cmc_token}
    r = requests.get(url, headers = headers, params=params).json()
    
    #BTC details
    name = r['data'][crypto]['name']
    symbol = r['data'][crypto]['symbol']
    
    #Data details
    cmc_rank = r['data'][crypto]['cmc_rank']
    max_supply = r['data'][crypto]['max_supply']
    total_supply = r['data'][crypto]['total_supply']
    circulating_supply = r['data'][crypto]['circulating_supply']
    
    #INR detials
    price = r['data'][crypto]['quote']['INR']['price']
    volume_24 = r['data'][crypto]['quote']['INR']['volume_24h']
    percent_change_1h = r['data'][crypto]['quote']['INR']['percent_change_1h']
    percent_change_24h = r['data'][crypto]['quote']['INR']['percent_change_24h']
    percent_change_7d = r['data'][crypto]['quote']['INR']['percent_change_7d']
    market_cap = r['data'][crypto]['quote']['INR']['market_cap']
    
    #returning required details
    def print_details():
        print("CoinMarketCap Ranking : ", cmc_rank)
        print("Name : ", name)
        print("Symbol : ", symbol)
        print("Current Price in INR : ₹ ", price)
        print("Market Cap in INR : ₹ ", market_cap)
        print("Volume last 24 hours : ", volume_24)
        print("Change in 1 hour : " + str(percent_change_1h)  + " %")
        print("Change in 24 hour : " + str(percent_change_24h) + " %")
        print("Change in 7 day : " + str(percent_change_7d) + " %")
    
    
    #Output
    return cmc_rank, name, symbol, price, market_cap, volume_24, percent_change_1h, percent_change_24h, percent_change_7d

#Telegram Parsing
def parse_message(message):
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']
    
    pattern = r'/[a-zA-Z]{2,4}'
    
    ticker = re.findall(pattern, txt)
    
    if ticker:
        symbol = ticker[0][1:].upper()
    else:
        symbol = ''
    return chat_id, symbol
    
    
#Send message function
def send_message(chat_id, text):
    url = 'https://api.telegram.org/bot948482927:AAEckZdqwfyrxcazcQLGAmFyXf3GNctg450/sendMessage'
    payload = {'chat_id' : chat_id, 'text': text}
    r = requests.post(url, json=payload)
    return r
    
#Flask route
@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, symbol = parse_message(msg)
        if not symbol:
            send_message(chat_id, 'Wrong symbol! Please, try again.')
            return Response('ok', status=200)
        
        price = getComaCap_Data(symbol)
        send_message(chat_id, [symbol, price])
        write_json(msg, 'telegram_request.json')
        return Response('ok', status = 200)
    else:
        return '<h1>Crystma Bot</h1> <h2>FUCKMA</h2>'

#Main function
def main():
    
    # TODO BOT
    #1) Locally create a basic flask application
    #2) Set up a tunnel
    #3) Set a webhook
    #4) Recieve and parse user message
    #5) Send message to user
    
    print("Start")
    #https://api.telegram.org/bot948482927:AAEckZdqwfyrxcazcQLGAmFyXf3GNctg450/getMe
    #https://api.telegram.org/bot948482927:AAEckZdqwfyrxcazcQLGAmFyXf3GNctg450/sendMessage?chat_id=399047912&text=Hello,user
    #https://api.telegram.org/bot948482927:AAEckZdqwfyrxcazcQLGAmFyXf3GNctg450/setWebhook?url=https://deyalla.pythonanywhere.com/


if __name__ == '__main__':
    #main()
    app.run(debug=True)