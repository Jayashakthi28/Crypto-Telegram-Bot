import telebot
import time
bot = telebot.TeleBot('1885999746:AAFYqE2yqSHb4x6fvwWDP9-cfSa0MheDIyw', parse_mode='HTML')
while(1):
    bot.send_message(-508156931,'/start')
    bot.polling()
    time.sleep(18000)
