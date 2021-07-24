import api
import telebot
import database as sqler
from binance.client import Client
import time
from datetime import datetime
import pytz
while 1:
    IST = pytz.timezone('Asia/Kolkata')
    bot = telebot.TeleBot(api.tak, parse_mode=None)
    chat_id=[]
    client = Client(api.binance_api_key, api.binance_sec_key)
    fav_coin_outer=[]
    mycursor=sqler.mydb.cursor()
    mycursor.execute('SELECT chat_id FROM fav_coin_table')
    result=mycursor.fetchall()
    coin_pair=["BTC","USDT","ETH","BNB","BUSD"]
    for i in result:
        for j in i:
            chat_id.append(j)
    for i in chat_id:
        fav_coin=[]
        mycursor.execute(f'SELECT fav_coins FROM fav_coin_table WHERE chat_id={i}')
        result=mycursor.fetchall()
        if result[0][0]!=None:
            text=f"COINS PRICE AS OF \n{datetime.now(IST).strftime('%d/%m/%Y--%H:%M')}\n\n"
            for j in result[0][0].split(" "):
                fav_coin.append(j.upper())
            for k in fav_coin:
                text+=f"{k} Price: \n"
                for z in coin_pair:
                    temp=k+z
                    try:
                        crypt_price = client.get_symbol_ticker(symbol=temp)
                        pstr=crypt_price['price']
                        if(pstr!=' '):
                            text+=f'{z} - '
                            text+=f"{pstr}\n"
                    except:
                        pass
                text+="\n"
        if(text!=None):
            try:
                bot.send_message(i,text)
            except:
                pass
    time.sleep(5000)
# for j in fav_coin_outer:
#     lister=[]
#     try:
#         j=j.split(" ")
#         for k in j:
#             lister.append(k.upper())
#     except:
#         break

    #bot.send_message(i,text)