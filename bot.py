import api
import telebot
import binance
from binance.client import Client
import datetime
import pytz
import database as sqler
import time
import requests
import json
import pyotp
import qrcode
from PIL import Image 
import random
from pyqrcode import QRCode

bot = telebot.TeleBot(api.tak, parse_mode='HTML')
client = Client(api.binance_api_key, api.binance_sec_key)
def auth_code_displayer(chat_id):
    totp_code=pyotp.random_base32()
    url=pyotp.totp.TOTP(totp_code).provisioning_uri(name='Crypto Jsv Telebot', issuer_name='Telegram')
    img=qrcode.make(totp_code)
    qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=30,
    border=20,
    )
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="orange", back_color="black").convert('RGB')
    bot.send_photo(chat_id,img,f'<code>{totp_code}</code>')
    bot.send_message(chat_id,"Just Scan the Qr Code or Copy the String to your Google Auth App")
    return totp_code
ignored_cmds=ignored_cmds=['/signup','/start@cypto_jsv_bot','/start','/fav','/fav@cypto_jsv_bot','/stop','/stop@cypto_jsv_bot','/signup@cypto_jsv_bot','/login','/login@cypto_jsv_bot','/logout','/logout@cypto_jsv_bot','/reset_pass','/reset_pass@cypto_jsv_bot','/weather','/weather@cypto_jsv_bot','/change_auth','/change_auth@cypto_jsv_bot','/modify_service','/modify_service@cypto_jsv_bot','/movie','/movie@cypto_jsv_bot','/super_hero','/super_hero@cypto_jsv_bot']
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if(m.text not in ignored_cmds):
            if m.content_type == 'text':
                text = m.text
                chatid=m.chat.id
                msg=text.upper()+" Price List"+"\n\n"
                list=['USDT','ETH','BTC','BNB','INR']
                for x in list:
                    temp=text.upper()+x
                    try:
                        btc_price = client.get_symbol_ticker(symbol=temp)
                        pstr=btc_price['price']
                        msg+=x+":"+pstr+"\n"
                    except:
                        pass
                if(msg!=text.upper()+" Price List"+"\n\n"):
                    bot.send_message(chatid, msg)
                else:
                    bot.send_message(chatid,"Sorry No Pair Found / Cannot Understand")
@bot.message_handler(commands=['signup'])
def signuper(message):
    sqler.list_updater()
    if(message.content_type=='text'):
        res=sqler.check_user(message.chat.id)
        if(res==2):
            msg=bot.send_message(message.chat.id,f'Username Already Exists with the Username <b><u>{sqler.query_getter("user_name",message.chat.id)}</u></b>\nDo you wanna Create new user by deleting current one(y/n) ?\n<code>Note:This Operation will logout all the Instances with this Username and Deletes the data..</code>')
            bot.register_next_step_handler(msg,confirm_user)
        elif(res==1):
            msg=bot.send_message(message.chat.id,f'Username Already Exists with the Username <b><u>{sqler.login_table_query("user_name","chat_id",message.chat.id)}</u></b>\n/logout and /signup')
        else:
            msg=bot.send_message(message.chat.id,'Enter Username')
            chat_id=message.chat.id
            sqler.chat_id_adder(chat_id)
            bot.register_next_step_handler(msg,user_checker)
    else:
        bot.send_message(message.chat.id,"Invalid Credentials")
def confirm_user(msg):
    if(msg.content_type=='text' and len(msg.text)<=255):
        if(msg.text.upper()=='Y'):
            try:
                sqler.logouter('user_name',msg.chat.id)
            except:
                pass
            sqler.delete_user_data(msg.chat.id)
            msg=bot.send_message(msg.chat.id,'Enter New Username')
            chat_id=msg.chat.id
            sqler.chat_id_adder(chat_id)
            bot.register_next_step_handler(msg,user_checker)
        elif(msg.text.upper()=='N'):
             bot.send_message(msg.chat.id,"Thank You")
        else:
            bot.send_message(msg.chat.id,"<b><i><u>Invalid Credentials</u></i></b>")
    else:
        bot.send_message(msg.chat.id,"<b><i><u>Invalid Credentials</u></i></b>")
def user_checker(msg):
    if(msg.content_type=='text'):
        if(sqler.user_name_checker(msg.text)==1):
            bot.send_message(msg.chat.id,"This Username is already Taken")
            msg=bot.send_message(msg.chat.id,"Enter a new user name")
            bot.register_next_step_handler(msg,user_checker)
        else:
            sqler.data_adder(msg.text,msg.chat.id,"user_name")
            msg=bot.send_message(msg.chat.id,'Enter Password')
            bot.register_next_step_handler(msg,fav_coin)
def fav_coin(msg):
    if(msg.content_type=='text'):
        sqler.data_adder(msg.text,msg.chat.id,"password")
        msg=bot.send_message(msg.chat.id,"Enter your favorite coins with space between\n eg: doge coti dodo (Like This)")
        bot.register_next_step_handler(msg,fav_getter)
    else:
        bot.send_message(msg.chat.id,"Sorry I dont accept Emojis and other stuff press \signup to try again")
def fav_getter(msg):
    sqler.data_adder(msg.text,msg.chat.id,"fav_coins")
    msg=bot.send_message(msg.chat.id,'Do you want to get Weather Updates Regularly?')
    bot.register_next_step_handler(msg,weather_choice_chooser)
def weather_choice_chooser(msg):
    if(msg.text.upper()=='Y' and len(msg.text)<=255):
        msg=bot.send_message(msg.chat.id,'Enter your Pin Code:')
        # url=f'https://api.openweathermap.org/data/2.5/weather?zip={msg.text},in&appid=b32de655e1d67335d82b9bdef75baae6&units=metric'
        # res=requests.get(url=url)
        # if(res.status_code!=200 or res.status_code!=201):
        #     msg.bot.
        bot.register_next_step_handler(msg,location_getter)
    elif(msg.text.upper()=='N'):
        bot.send_message(msg.chat.id,"User Created Successfully...Enter the 2 factor authentication  and /login to Proceed")
        msg=bot.send_message(msg.chat.id,f"Enter the 2 factor Auth Type:\n1)OTP\n2)Google Auth Code\nEnter 1 or 2")
        bot.register_next_step_handler(msg,auth_type_getter)
    else:
        bot.send_message(msg.chat.id,"Invalid Credentials...")
def location_getter(msg):
    time.sleep(0.1)
    url=f'https://api.openweathermap.org/data/2.5/weather?zip={msg.text},in&appid=b32de655e1d67335d82b9bdef75baae6&units=metric'
    res=requests.get(url=url)
    if(res.status_code!=200 and res.status_code!=201):
        msg=bot.send_message(msg.chat.id,"Sorry Please..Enter correct pincode../..Enter new Location")
        bot.register_next_step_handler(msg,location_getter)
    else:
        sqler.data_adder(msg.text,msg.chat.id,'weather_pin_code')
        bot.send_message(msg.chat.id,"User Created Successfully...Enter the 2 factor authentication  and /login to Proceed")
        msg=bot.send_message(msg.chat.id,f"Enter the 2 factor Auth Type:\n1)OTP\n2)Google Auth Code\nEnter 1 or 2")
        bot.register_next_step_handler(msg,auth_type_getter)
@bot.message_handler(commands=['start'])
def welcome(msg):
    bot.send_message(msg.chat.id,f"Hello {msg.chat.username if (msg.chat.username!=None) else 'User'} ✋ Welcome to the our Bot..\n/signup to <b>Signup</b> to Enjoy our Service\n/login to <b>Login</b>")
    bot.send_message(msg.chat.id,f"Just type the crypto name and you will get the price of the crypto...\nPlease /signup to get maximum out of our service\nThese are the commands of the bot:\n/start - <code>to start the bot</code>\n/signup - <code>to signup to the bot</code>\n/login - <code>to login to the bot</code>\n/logout - <code>to logout to the bot</code>\n/reset_pass - <code>to reset the password for your current account</code>\n/weather - <code>to get the weather info by pincode</code>\n/change_auth - <code>to change the two factor authentication type</code>\n/modify_service - <code>to list of your subscriptions</code>\n/movie - <code>to list the details about a movie</code>\n/super_hero - <code>Get Informations about Super Heros</code>")
@bot.message_handler(commands=['fav'])
def fav(msg):
    try:
        chat_id=sqler.main_chat_id_getter(msg.chat.id)
    except:
        chat_id=0
    if(chat_id!=0):
        txt=sqler.fav_coins_query_getter('fav_coins','chat_id',msg.chat.id)
        chat_id=sqler.main_chat_id_getter(msg.chat.id)
        try:
            weather=sqler.query_getter('weather_pin_code',chat_id)
        except:
            weather=0
        if(txt!=0 and txt!=None):
            bot.send_message(msg.chat.id,f'<strong>Hello {sqler.fav_coins_query_getter("user_name","chat_id",msg.chat.id)} ✋ Your Favorite Coins Are:\n<code>{txt}</code></strong>')
            if(weather!=0 and weather!=None and weather!='0000'):
                bot.send_message(msg.chat.id,f'Your Area Pin code for weather update is: {weather}')
            bot.send_message(msg.chat.id,f'/modify_service to modify your favourite data')
        elif(msg.chat.id not in sqler.login_list):
            bot.send_message(msg.chat.id,f'Hello {msg.chat.username if (msg.chat.username!=None) else "User"} ✋../login to avail this feature')
        elif(msg.chat.id not in sqler.id_list):
            bot.send_message(msg.chat.id,f'Hello {msg.chat.username if (msg.chat.username!=None) else "User"} ✋../signup to avail this feature')
    else:
         bot.send_message(msg.chat.id,f'Hello {msg.chat.username if (msg.chat.username!=None) else "User"} ✋../login to avail this feature')
@bot.message_handler(commands=['login'])
def login(msg):
    try:
        sqler.list_updater()
        if(sqler.login_table_query("user_name","chat_id",msg.chat.id)==None):
            sqler.login_table_deleter('chat_id',msg.chat.id)
            sqler.list_updater()
    except:
        pass
    if(msg.chat.id in sqler.login_list and sqler.login_table_query('status','chat_id',msg.chat.id)==1):
        bot.send_message(msg.chat.id,f'You have already Logged in as {sqler.login_table_query("user_name","chat_id",msg.chat.id)} /logout to logut and /login again')
    else:
        try:
            sqler.login_table_deleter('chat_id',msg.chat.id)
        except:
            pass
        m=bot.send_message(msg.chat.id,f'Enter UserName:')
        sqler.login_table_chat_id_add('chat_id',msg.chat.id)
        bot.register_next_step_handler(msg,user_name_getter)
def user_name_getter(msg):
    sqler.list_updater()
    if(msg.text not in sqler.user_name):
        bot.send_message(msg.chat.id,'Sorry no User found! /signup to create a new one')
        sqler.login_table_deleter('chat_id',msg.chat.id)
        sqler.list_updater()
    else:
        sqler.login_table_user_name_add(msg.text,msg.chat.id)
        msg=bot.send_message(msg.chat.id,"Enter Password")
        bot.register_next_step_handler(msg,password_getter)
def password_getter(msg):
    sqler.list_updater()
    res=sqler.password_checker(msg.chat.id)
    if(res==msg.text):
        if(sqler.login_table_status_add(msg.chat.id)==1):
            bot.send_message(msg.chat.id,"Successfully Logged in...")
            sqler.fav_coins_inserter(msg.chat.id)
            if(sqler.query_getter('auth',msg.chat.id)==None):
                msg=bot.send_message(msg.chat.id,f"Enter the 2 factor Auth Type:\n1)OTP\n2)Google Auth Code\nEnter 1 or 2")
                bot.register_next_step_handler(msg,auth_type_getter)
        else:
            sqler.login_table_deleter('chat_id',msg.chat.id)
            bot.send_message(msg.chat.id,'Sorry You Havent Logged in Yet!...Please Try Again!')
            sqler.list_updater()
    else:
        bot.send_message(msg.chat.id,'Wrong Password...Please try again /login to continue')
        sqler.login_table_deleter('chat_id',msg.chat.id)
        sqler.list_updater()
def auth_type_getter(msg):
    if(msg.text !='1' and msg.text!='2'):
        bot.send_message(msg.chat.id,"Sorry Wrong Option...")
        msg=bot.send_message(msg.chat.id,f"Enter the 2 factor Auth Type:\n1)OTP\n2)Google Auth Code\nEnter 1 or 2")
        bot.register_next_step_handler(msg,auth_type_getter)
    elif(msg.text=='1'):
        sqler.data_adder(1,msg.chat.id,'auth')
        bot.send_message(msg.chat.id,"Successfully Added 2 Factor Authentication")
    elif(msg.text=='2'):
        try:
            sqler.gauth_deleter(msg.chat.id)
        except:
            pass
        sqler.gauth_inserter(msg.chat.id,auth_code_displayer(msg.chat.id))
        msg=bot.send_message(msg.chat.id,"Enter the TOTP in your auth App")
        bot.register_next_step_handler(msg,otp_verifier)
def otp_verifier(msg):
    totp_code=sqler.gauth_query_getter('auth_code','chat_id',msg.chat.id)
    totp = pyotp.TOTP(totp_code).now()
    if(totp==msg.text):
        bot.send_message(msg.chat.id,"Successfully Added the Authentication.../change_auth to change auth type")
        sqler.data_adder(2,msg.chat.id,'auth')
    else:
        msg=bot.send_message(msg.chat.id,"Sorry Might be timed out...Please ReEnter the TOTP from Google Auth App")
        bot.register_next_step_handler(msg,otp_verifier)
@bot.message_handler(commands=['logout'])
def logout(msg):
    sqler.list_updater()
    if(msg.chat.id not in sqler.login_list):
        bot.send_message(msg.chat.id,"You Haven't /login yet..!!")
    elif(sqler.login_table_query('status','chat_id',msg.chat.id)==1):
        bot.send_message(msg.chat.id,f'You are Logged in as {sqler.login_table_query("user_name","chat_id",msg.chat.id)}')
        msg=bot.send_message(msg.chat.id,f'Enter Password:')
        bot.register_next_step_handler(msg,logout_password_getter)
    else:
        sqler.login_table_deleter('chat_id',msg.chat.id)
        bot.send_message(msg.chat.id,"You Haven't /login yet..!!")
def logout_password_getter(msg):
    sqler.list_updater()
    if(msg.chat.id in sqler.login_list):
        res=sqler.password_checker(msg.chat.id)
        if(msg.text==res):
            if(sqler.check_user(msg.chat.id)==2):
                msg=bot.send_message(msg.chat.id,'Do you want logout of:\n1)This Instance\n2)All Instance\n(Eg:Type either 1 or 2)')
                bot.register_next_step_handler(msg,logout_choice_chooser)
            elif(sqler.check_user(msg.chat.id)==1):
                if(sqler.logouter('chat_id',msg.chat.id)==1):
                    sqler.list_updater()
                    bot.send_message(msg.chat.id,'Successfully Logged Out...')
                else:
                    bot.send_message(msg.chat.id,"Sorry Something Went Wrong...Might be Another user Logged Out of all Instances...")        
            else:
                bot.send_message(msg.chat.id,'You havebeen Logged Out by other User...')
        else:
            bot.send_message(msg.chat.id,f'Wrong Password...Please Try /logout Again!!!')
    else:
        bot.send_message(msg.chat.id,"Sorry Something Went Wrong...Might be Another user Logged Out of all Instances...")
def logout_choice_chooser(msg):
    sqler.list_updater()
    if(msg.chat.id in sqler.login_list):
        if(msg.text=='1'):
            if(sqler.logouter('chat_id',msg.chat.id)==1):
                sqler.list_updater()
                bot.send_message(msg.chat.id,'Successfully Logged Out...')
        elif (msg.text=='2'):
            if(sqler.logouter('user_name',msg.chat.id)==1):
                sqler.list_updater()
                bot.send_message(msg.chat.id,'Successfully Logged of All Instances...')
        else:
            bot.send_message(msg.chat.id,"Sorry Wrong option../logout again")
    else:
         bot.send_message(msg.chat.id,"Sorry Something Went Wrong...Might be Another user Logged Out of all Instances...")
@bot.message_handler(commands=['change_auth'])
def change_auth(msg):
    sqler.list_updater()
    if(msg.chat.id in sqler.login_list):
        chat_id=sqler.main_chat_id_getter(msg.chat.id)
        auth_type=sqler.query_getter('auth',chat_id)
        if(auth_type==1):
            bot.send_message(msg.chat.id,"You have OTP as the Current Authentication Step...Which will be Changed Now")
            msg=bot.send_message(msg.chat.id,"Enter the Otp Sent to your Main Account")
            txt=random.randint(1111,9999)
            sqler.add_otp(msg.chat.id,txt)
            bot.send_message(chat_id,f"The otp is <code>{txt}</code>")
            bot.register_next_step_handler(msg,otp_checker)
        elif(auth_type==2):
            bot.send_message(msg.chat.id,"You have TOTP(Google Authenticator) as the Current Authentication Step...Which will be Changed Now")
            msg=bot.send_message(msg.chat.id,"Enter the Totp in your Gauth App")
            bot.register_next_step_handler(msg,totp_checker)
    else:
        bot.send_message(msg.chat.id,"You must /login to change the Authentication Type...")
def otp_checker(msg):
    txt=sqler.otp_getter(msg.chat.id)
    if(str(msg.text)==str(txt)):
        bot.send_message(msg.chat.id,'Otp is correct')
        totp_code=auth_code_displayer(msg.chat.id)
        chat_id=sqler.main_chat_id_getter(msg.chat.id)
        sqler.gauth_inserter(chat_id,totp_code)
        msg=bot.send_message(msg.chat.id,"Enter the Totp from the Gauth App")
        bot.register_next_step_handler(msg,otp_verifier)
    else:
        bot.send_message(msg.chat.id,"Otp is wrong...Please /change_auth again")
def totp_checker(msg):
    totp_code=sqler.gauth_query_getter('auth_code','chat_id',msg.chat.id)
    totp = pyotp.TOTP(totp_code).now()
    if(msg.text==totp):
        bot.send_message(msg.chat.id,"Totp is Correct...")
        chat_id=sqler.main_chat_id_getter(msg.chat.id)
        sqler.data_adder(1,chat_id,'auth')
        sqler.gauth_deleter(chat_id)
        bot.send_message(msg.chat.id,"Authentication type Changed to <b><i>OTP</i></b>....")
    else:
        bot.send_message(msg.chat.id,"Otp is wrong...Please /change_auth again")
@bot.message_handler(commands=['reset_pass'])
def password_reset_step1(msg):
    msg=bot.send_message(msg.chat.id,'Please Enter the UserName')
    bot.register_next_step_handler(msg,auth_type_checker)
def auth_type_checker(msg):
    try:
        chat_id=sqler.main_chat_id_getter_user_name(msg.text)
    except:
        chat_id=0
        bot.send_message(msg.chat.id,"Sorry No Username Found")
    if(chat_id!=0):
        sqler.password_reset_table_inserter(msg.text,msg.chat.id)
        auth_type=sqler.query_getter('auth',chat_id)
        if(auth_type==1):
            msg=bot.send_message(msg.chat.id,"Enter the Otp Sent to your Main Account")
            txt=random.randint(1111,9999)
            sqler.add_otp(msg.chat.id,txt)
            bot.send_message(chat_id,f"The otp is <code>{txt}</code>")
            bot.register_next_step_handler(msg,reset_otp_checker)
        elif(auth_type==2):
            msg=bot.send_message(msg.chat.id,"Enter the Totp in your Gauth App")
            bot.register_next_step_handler(msg,reset_totp_checker)
def reset_otp_checker(msg):
    txt=sqler.otp_getter(msg.chat.id)
    if(str(msg.text)==str(txt)):
        bot.send_message(msg.chat.id,'Otp is Correct')
        msg=bot.send_message(msg.chat.id,'Enter The New Password...')
        bot.register_next_step_handler(msg,new_password_assigner)
    else:
        bot.send_message(msg.chat.id,'Otp is Wrong...Try Again!')
        sqler.password_reset_table_deleter(msg.chat.id)
def reset_totp_checker(msg):
    totp_code=sqler.gauth_query_getter('auth_code','chat_id',msg.chat.id)
    totp = pyotp.TOTP(totp_code).now()
    if(msg.text==totp):
        bot.send_message(msg.chat.id,"Totp is Correct...")
        msg=bot.send_message(msg.chat.id,'Enter The New Password...')
        bot.register_next_step_handler(msg,new_password_assigner)
    else:
        bot.send_message(msg.chat.id,"Totp is Wrong..Please Try Again")
        sqler.password_reset_table_deleter(msg.chat.id)
# def password_reset(msg):
#     if(sqler.password_reset(msg.chat.id,msg.text)==1):
#         msg=bot.send_message(msg.chat.id,"Please Enter the New Password")
#         bot.register_next_step_handler(msg,new_password_assigner)
#     elif(msg.text not in sqler.user_name):
#         bot.send_message(msg.chat.id,"No user found with the Entered User Name...")
#     else:
#         sqler.list_updater()
#         bot.send_message(msg.chat.id,"Only The Instance in which this User is created has the Access to Reset this User's Password")
#         res=sqler.query_getter('user_name',msg.chat.id)
#         if res!=0:
#             bot.send_message(msg.chat.id,f"You have the rights to reset Password for {res}")
def new_password_assigner(msg):
    sqler.list_updater()
    user_name=sqler.password_reset_query('user_name','chat_id',msg.chat.id)
    chat_id=sqler.main_chat_id_getter_user_name(user_name)
    sqler.new_password_setter(chat_id,msg.text)
    try:
        sqler.logouter('user_name',msg.chat.id)
    except:
        pass
    sqler.list_updater()
    bot.send_message(msg.chat.id,"Successfully Reseted the Password and Logged out of all instances")
    sqler.password_reset_table_deleter(msg.chat.id)
@bot.message_handler(commands=['weather'])
def weather(msg):
    msg=bot.send_message(msg.chat.id,"Enter your Pincode-->")
    bot.register_next_step_handler(msg,weather_getter)
def weather_getter(msg):
    text=''
    time.sleep(0.1)
    url=f'https://api.openweathermap.org/data/2.5/weather?zip={msg.text},in&appid=b32de655e1d67335d82b9bdef75baae6&units=metric'
    res=requests.get(url=url)
    if(res.status_code==200 or res.status_code==201):
        data=res.json()
        text+=f"Weather at <b><u>{data['name']}</u></b>:\n\nWeather is like <b>{data['weather'][0]['description']}</b>\nTemperature is <b>{data['main']['temp']}{chr(176)}C</b>"
        bot.send_message(msg.chat.id,text)
    else:
        bot.send_message(msg.chat.id,"Sorry No Location Found")
@bot.message_handler(commands=['modify_service'])
def modify_auth_type_checker(msg):
    try:
        chat_id=sqler.main_chat_id_getter(msg.chat.id)
    except:
        chat_id=0
        bot.send_message(msg.chat.id,"You must /login")
    if(chat_id!=0):
        auth_type=sqler.query_getter('auth',chat_id)
        if(auth_type==1):
            msg=bot.send_message(msg.chat.id,"Enter the Otp Sent to your Main Account")
            txt=random.randint(1111,9999)
            sqler.add_otp(msg.chat.id,txt)
            bot.send_message(chat_id,f"The otp is <code>{txt}</code>")
            bot.register_next_step_handler(msg,modify_otp_checker)
        elif(auth_type==2):
            msg=bot.send_message(msg.chat.id,"Enter the Totp in your Gauth App")
            bot.register_next_step_handler(msg,modify_totp_checker)
def modify_otp_checker(msg):
    txt=sqler.otp_getter(msg.chat.id)
    if(str(msg.text)==str(txt)):
        bot.send_message(msg.chat.id,'Otp is Correct')
        msg=bot.send_message(msg.chat.id,f"Enter the Service that you want to modify:<b><i>\n1)Favorite Coins\n2)Weather Service</i></b>\n<code>Enter 1 or 2</code>")
        bot.register_next_step_handler(msg,modify_choice_chooser)
    else:
        bot.send_message(msg.chat.id,'Otp is Wrong...Try Again!')
        sqler.password_reset_table_deleter(msg.chat.id)
def modify_totp_checker(msg):
    totp_code=sqler.gauth_query_getter('auth_code','chat_id',msg.chat.id)
    totp = pyotp.TOTP(totp_code).now()
    if(msg.text==totp):
        bot.send_message(msg.chat.id,"Totp is Correct...")
        msg=bot.send_message(msg.chat.id,f"Enter the Service that you want to modify:<b><i>\n1)Favorite Coins\n2)Weather Service</i></b>\n<code>Enter 1 or 2</code>")
        bot.register_next_step_handler(msg,modify_choice_chooser)
    else:
        bot.send_message(msg.chat.id,"Totp is Wrong..Please Try Again")
        sqler.password_reset_table_deleter(msg.chat.id)
def modify_choice_chooser(msg):
    if(msg.text=='1'):
        chat_id=sqler.main_chat_id_getter(msg.chat.id)
        fav_coins=sqler.query_getter('fav_coins',chat_id)
        bot.send_message(msg.chat.id,f"Your Favorite Coins are:\n<code>{fav_coins}</code>")
        bot.send_message(msg.chat.id,"This will be modified now..")
        msg=bot.send_message(msg.chat.id,"Enter your favorite coins with space separated...\nLike: <code>dodo coti doge btc</code>")
        bot.register_next_step_handler(msg,fav_coins_getter)
    elif(msg.text=='2'):
        chat_id=sqler.main_chat_id_getter(msg.chat.id)
        msg=bot.send_message(msg.chat.id,'Do you want to get Weather Updates Regularly?')
        bot.register_next_step_handler(msg,modify_weather_choice_chooser)
    elif(msg.text=='0'):
        bot.send_message(msg.chat.id,"Thank You!!")
    else:
        bot.send_message(msg.chat.id,"<b><i><u>Invalid Credentials</u></i></b>")   
def fav_coins_getter(msg):
    chat_id=sqler.main_chat_id_getter(msg.chat.id)
    sqler.data_adder(msg.text,chat_id,'fav_coins')
    sqler.fav_coins_deleter('user_name',msg.chat.id)
    sqler.fav_coins_inserter(msg.chat.id)
    bot.send_message(msg.chat.id,"Your Favourite coins are updated /fav to see them")
    msg=bot.send_message(msg.chat.id,f"Enter the Service that you want to modify:<b><i>\n1)Favorite Coins\n2)Weather Service</i></b>\n<code>Enter 1 or 2 and 0 For Quiting</code>")
    bot.register_next_step_handler(msg,modify_choice_chooser)

def modify_weather_choice_chooser(msg):
    if(msg.text.upper()=='Y' and len(msg.text)<=255):
        msg=bot.send_message(msg.chat.id,'Enter your Pin Code:')
        bot.register_next_step_handler(msg,modify_location_getter)
    elif(msg.text.upper()=='N'):
        chat_id=sqler.main_chat_id_getter(msg.chat.id)
        sqler.data_adder('0000',chat_id,'weather_pin_code')
        bot.send_message(msg.chat.id,'Thank You')
        msg=bot.send_message(msg.chat.id,f"Enter the Service that you want to modify:<b><i>\n1)Favorite Coins\n2)Weather Service</i></b>\n<code>Enter 1 or 2 and 0 For Quiting</code>")
        bot.register_next_step_handler(msg,modify_choice_chooser)
    else:
        bot.send_message(msg.chat.id,"Invalid Credentials...")
def modify_location_getter(msg):
    url=f'https://api.openweathermap.org/data/2.5/weather?zip={msg.text},in&appid=b32de655e1d67335d82b9bdef75baae6&units=metric'
    time.sleep(1)
    res=requests.get(url=url)
    if(res.status_code!=200 and res.status_code!=201):
        msg=bot.send_message(msg.chat.id,"Sorry Please..Enter correct pincode../Enter new Location")
        bot.register_next_step_handler(msg,location_getter)
    else:
        chat_id=sqler.main_chat_id_getter(msg.chat.id)
        sqler.data_adder(msg.text,chat_id,'weather_pin_code')
        bot.send_message(msg.chat.id,"Location updated successfully..")
        msg=bot.send_message(msg.chat.id,f"Enter the Service that you want to modify:<b><i>\n1)Favorite Coins\n2)Weather Service</i></b>\n<code>Enter 1 or 2 and 0 For Quiting</code>")
        bot.register_next_step_handler(msg,modify_choice_chooser)
@bot.message_handler(commands=['movie'])
def movie(msg):
    msg=bot.send_message(msg.chat.id,"Enter the <u><b>movie/series</b></u> name")
    bot.register_next_step_handler(msg,movie_name_getter)
def movie_name_getter(msg):
    time.sleep(0.1)
    try:
        url=f'https://www.omdbapi.com/?t={msg.text.lower()}&apikey=63979af2'
        res=requests.get(url=url)
        data=res.json()
        text=''
        if(data['Response']!='False'):
            text+=f"<b>Name:</b>   <code>{data['Title']}</code>\n\n<b>Rating:</b>  <code>{data['Rated']}</code>\n\n<b>Cast:</b>   <code>{data['Actors']}</code>\n\n<b>Languages:</b> <code>{data['Language']}</code>\n\n<b>Director:</b>    <code>{data['Director']}</code>\n\n<b>Released Year:</b>  <code>{data['Released']}</code>\n\n<b>Genre:</b>   <code>{data['Genre']}</code>\n\n<b>IMDB Rating:</b>    <code>{data['imdbRating']}</code>\n\n{data['Poster']}"
            bot.send_message(msg.chat.id,text)
        else:
            bot.send_message(msg.chat.id,"Sorry no movie found in this name please check the spelling and /movie again")
    except:
        bot.send_message(msg.chat.id,"Sorry the Movie Service is down..Please try again after some time")
@bot.message_handler(commands=['super_hero'])
def super_hero(msg):
     msg=bot.send_message(msg.chat.id,"Enter the <u><b>Super Hero Name</b></u> ")
     bot.register_next_step_handler(msg,super_hero_getter)
def super_hero_getter(msg):
    time.sleep(0.1)
    url=f'https://www.superheroapi.com/api.php/1497111163953845/search/{msg.text.lower()}'
    Response=requests.get(url=url)
    data=Response.json()
    text=''
    if(data['response']!='error'):
        text+=f"Name:   <code>{data['results'][0]['name']}</code>\n\nFull-Name:    <code>{data['results'][0]['biography']['full-name']}</code>\n\nStrength:   <code>{data['results'][0]['powerstats']['strength']}</code>\n\nIntelligence:    <code>{data['results'][0]['powerstats']['intelligence']}</code>\n\nSpeed:    <code>{data['results'][0]['powerstats']['speed']}</code>\n\nDurability:    <code>{data['results'][0]['powerstats']['durability']}</code>\n\nPower:    <code>{data['results'][0]['powerstats']['power']}</code>\n\nOther Names:    <code>{' , '.join(data['results'][0]['biography']['aliases'])}</code>\n\n\
Place of Birth:    <code>{data['results'][0]['biography']['place-of-birth']}</code>\n\n\
First Apperance:    <code>{data['results'][0]['biography']['first-appearance']}</code>\n\n\
Gender:    <code>{data['results'][0]['appearance']['gender']}</code>\n\n\
Height:    <code>{data['results'][0]['appearance']['height'][1]}</code>\n\n\
Weight:    <code>{data['results'][0]['appearance']['weight'][1]}</code>\n\n\
Occupation:    <code>{data['results'][0]['work']['occupation']}</code>\n\n\
Group-Affilication:    <code>{data['results'][0]['connections']['group-affiliation']}</code>\n\n\
Relatives:  <code>{data['results'][0]['connections']['relatives']}</code>\n\n\
{data['results'][0]['image']['url']}"
        bot.send_message(msg.chat.id,text)
    else:
        bot.send_message(msg.chat.id,'Sorry No Super Hero found..!../super_hero again')
bot.set_update_listener(listener)
time.sleep(1)
bot.polling()
# bot.polling(none_stop=True)
# bot.polling(interval=3)

# while True:
#     pass