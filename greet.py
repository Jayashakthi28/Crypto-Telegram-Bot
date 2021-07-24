import datetime
import pytz
import api
import telebot
import time
import database as sqler
import requests
import time
while 1:
    bot = telebot.TeleBot(api.tak, parse_mode='HTML')
    sqler.list_updater()
    IST = pytz.timezone('Asia/Kolkata')
    datetime_ist = datetime.datetime.now(IST).strftime('%H')
    greet_list=[]
    for x in sqler.id_list:
        greet_list.append(x)
    for x in sqler.login_list:
        greet_list.append(x)
    greet_list=set(greet_list)
    for chat_id in greet_list:
        url='https://inspiration.goprogram.co.uk'
        time.sleep(0.01)
        response=requests.get(url=url)
        data=response.json()
        if(datetime_ist=='8'):
            text=f'<b><i>{data["quote"]}</i></b>\n\n<b>Good Morning! Have a nice Day...</b>'
            bot.send_message(chat_id,text)
        elif(datetime_ist=="13"):
            text=f'<b><i>{data["quote"]}</i></b>\n\n<b>Good Afternoon! Work Hard...</b>'
            bot.send_message(chat_id,text)
        elif(datetime_ist=="17"):
            text=f'<b><i>{data["quote"]}</i></b>\n\n<b>Good Evening! Relax Your Day...</b>'
            bot.send_message(chat_id,text)
        if(datetime_ist=="20"):
            text=f'<b><i>{data["quote"]}</i></b>\n\n<b>Good Night! Sweet Dreams...</b>'
            bot.send_message(chat_id,text)
    time.sleep(320)
    sqler.list_updater()
    for chat_id in sqler.login_list:
        sql=f'SELECT status FROM login_table WHERE chat_id=(%s)'
        val=(chat_id,)
        sqler.mycursor.execute(sql,val)
        res=sqler.mycursor.fetchall()[0][0]
        if(res==1):
            sql='SELECT user_name FROM login_table WHERE chat_id=(%s)'
            val=(chat_id,)
            sqler.mycursor.execute(sql,val)
            try:
                res=sqler.mycursor.fetchall()[0][0]
                sql=f'SELECT weather_pin_code FROM telebot WHERE user_name=(%s)'
                val=(res,)
                sqler.mycursor.execute(sql,val)
                msg=sqler.mycursor.fetchall()[0][0]
                text=''
                time.sleep(0.1)
                url=f'https://api.openweathermap.org/data/2.5/weather?zip={msg},in&appid=b32de655e1d67335d82b9bdef75baae6&units=metric'
                response=requests.get(url=url)
                if(response.status_code==200 or response.status_code==201):
                    data=response.json()
                    text+=f"Weather at <b><i><u>{data['name']}</u></i></b>:\n\nWeather is like <b><i>{data['weather'][0]['description']}</i></b>\nTemperature is <b>{data['main']['temp']}{chr(176)}C</b>"
                    bot.send_message(chat_id,text)
            except:
                pass
    time.sleep((60-int(datetime.datetime.now(IST).strftime('%M')))*60)