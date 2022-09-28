import psycopg2

mydb = psycopg2.connect(
  host="dpg-ccpr1b2en0hr84ne97v0-a",
  database="crypto_telegram_bot_db",
  user="crypto_telegram_bot_db_user",
  password="MME0mKjDWvE3ushDhNusLGokqfFrQgDk",
  port="5432"
)
# mydb = psycopg2.connect(
#   host="localhost",
#   database="telebot",
#   user="jsv",
#   password="2811",
# )
mycursor = mydb.cursor()
id_list=[]
user_name=[]
login_list=[]
def list_updater():
  global login_list
  global id_list
  global user_name
  login_list=[]
  mycursor.execute("SELECT chat_id FROM telebot")
  myresult = mycursor.fetchall()
  for i in myresult:
    for j in i:
      id_list.append(j)
  id_list=list(dict.fromkeys(id_list))
  mycursor.execute("SELECT chat_id FROM login_table")
  myresult = mycursor.fetchall()
  for i in myresult:
    for j in i:
      login_list.append(j)
  login_list=list(dict.fromkeys(login_list))
  mycursor.execute("SELECT user_name FROM telebot")
  myresult=mycursor.fetchall()
  for i in myresult:
    for j in i:
      user_name.append(j)
  user_name=list(dict.fromkeys(user_name))
def check_user(chat_id):
  global id_list
  global login_list
  if chat_id in login_list and (login_table_query('user_name','chat_id',chat_id)==query_getter('user_name',chat_id)):
    return 2
  elif (chat_id in id_list):
    return 2
  elif (chat_id in login_list):
    return 1
  return 0

def delete_user_data(chat_id):
  sql="DELETE FROM telebot where chat_id = %s"
  val=(chat_id,)
  mycursor.execute(sql,val)
  mydb.commit()
def user_name_checker(user_name):
  try:
    mycursor.execute("SELECT user_name FROM telebot")
    user_namer=mycursor.fetchall()
    for i in user_namer:
      for j in i:
        if(user_name==j):
          return 1
  except:
    return 0
def chat_id_adder(chatid):
    sql=f"INSERT INTO telebot (chat_id) VALUES (%s)"
    val=(chatid,)
    mycursor.execute(sql,val)
    mydb.commit()

def data_adder(data,chatid,data_col_name):
    sql=f'UPDATE telebot SET {data_col_name}=(%s) WHERE chat_id=(%s)'
    val=(data,chatid)
    mycursor.execute(sql,val)
    mydb.commit()

def query_getter(col_name,chat_id):
  list_updater()
  if chat_id in id_list:
    sql=f'SELECT {col_name} FROM telebot WHERE chat_id=(%s)'
    val=(chat_id,)
    mycursor.execute(sql,val)
    res=mycursor.fetchall()
    return res[0][0]
  else:
    return 0
def login_table_query(col_name,attribute_name,value):
  sql=f'SELECT {col_name} FROM login_table WHERE {attribute_name}=(%s)'
  val=(value,)
  mycursor.execute(sql,val)
  res=mycursor.fetchall()[0][0]
  return res
def login_table_chat_id_add(col_name,value):
  sql=f'INSERT INTO login_table ({col_name}) VALUES (%s)'
  val=(value,)
  mycursor.execute(sql,val)
  mydb.commit()
def login_table_user_name_add(chat_id,user_name):
  sql=f'UPDATE login_table SET user_name=(%s) WHERE chat_id=(%s)'
  val=(chat_id,user_name)
  mycursor.execute(sql,val)
  mydb.commit()
def login_table_deleter(col_name,value):
  sql=f'DELETE FROM login_table WHERE {col_name}=(%s)'
  val=(value,)
  mycursor.execute(sql,val)
  mydb.commit()
def password_checker(chat_id):
  sql=f'SELECT user_name FROM login_table WHERE chat_id=(%s)'
  val=(chat_id,)
  mycursor.execute(sql,val)
  myresut=mycursor.fetchall()[0][0]
  if(myresut!=None):
    sql=f'SELECT password FROM telebot WHERE user_name=(%s)'
    val=(myresut,)
    mycursor.execute(sql,val)
    myresut=mycursor.fetchall()[0][0]
    if(myresut!=None):
      return myresut
    return -1
  else:
    return -2
def logouter(attribute,value):
  if(attribute=='chat_id'):
    fav_coins_deleter('chat_id',value)
    sql=f'DELETE FROM login_table WHERE ({attribute})=(%s)'
    val=(value,)
    mycursor.execute(sql,val)
    mydb.commit()
    return 1
  elif(attribute=='user_name'):
    fav_coins_deleter('user_name',value)
    res=login_table_query('user_name','chat_id',value)
    sql=f'DELETE FROM login_table WHERE ({attribute})=(%s)'
    val=(res,)
    mycursor.execute(sql,val)
    mydb.commit()
    return 1
  return 0
def password_reset(chat_id,user_name):
  list_updater()
  res=query_getter('user_name',chat_id)
  if(res==user_name):
    return 1
  else:
    return 0
def new_password_setter(chat_id,password):
  sql=f'UPDATE telebot SET password=(%s) WHERE chat_id=(%s)'
  val=(password,chat_id)
  mycursor.execute(sql,val)
  mydb.commit()
def fav_coins_inserter(chat_id):
  user_name=login_table_query('user_name','chat_id',chat_id)
  sql=f'SELECT fav_coins FROM telebot WHERE user_name=(%s)'
  val=(user_name,)
  mycursor.execute(sql,val)
  fav_coins=mycursor.fetchall()[0][0]
  sql=f'INSERT INTO fav_coin_table (chat_id,user_name,fav_coins) VALUES (%s,%s,%s)'
  val=(chat_id,user_name,fav_coins)
  mycursor.execute(sql,val)
  mydb.commit()
def fav_coins_deleter(attribute,value):
  if(attribute=='chat_id'):
    sql=f'DELETE FROM fav_coin_table WHERE chat_id=(%s)'
    val=(value,)
    mycursor.execute(sql,val)
    mydb.commit()
  elif(attribute=='user_name'):
    res=login_table_query('user_name','chat_id',value)
    sql=f'DELETE FROM fav_coin_table WHERE ({attribute})=(%s)'
    val=(res,)
    mycursor.execute(sql,val)
    mydb.commit()
def fav_coins_query_getter(col_name,attribute,value):
  sql=f'SELECT {col_name} FROM fav_coin_table WHERE {attribute}=(%s)'
  val=(value,)
  mycursor.execute(sql,val)
  res=mycursor.fetchall()
  if(res!=[]):
    return res[0][0]
  else:
    return 0
def login_table_status_add(chat_id):
  if(login_table_query('user_name','chat_id',chat_id)!=None):
    sql=f'UPDATE login_table SET status=(%s) WHERE chat_id=(%s)'
    val=(1,chat_id)
    mycursor.execute(sql,val)
    mydb.commit()
    return 1
  else:
    return 0
def gauth_inserter(chat_id,totp_code):
  list_updater()
  if(chat_id not in id_list):
    user_name=login_table_query('user_name','chat_id',chat_id)
    sql=f'SELECT chat_id FROM telebot WHERE user_name=(%s)'
    val=(user_name,)
    mycursor.execute(sql,val)
    res=mycursor.fetchall()[0][0]
    sql=f'INSERT into gauth VALUES(%s,%s)'
    val=(res,totp_code)
    mycursor.execute(sql,val)
    mydb.commit()
  else:
    sql=f'INSERT into gauth VALUES(%s,%s)'
    val=(chat_id,totp_code)
    mycursor.execute(sql,val)
    mydb.commit()
def gauth_query_getter(col_name,attribute,value):
  sql=f'SELECT {col_name} FROM gauth WHERE {attribute}=(%s)'
  val=(value,)
  mycursor.execute(sql,val)
  return mycursor.fetchall()[0][0]
def main_chat_id_getter(chat_id):
    user_name=login_table_query('user_name','chat_id',chat_id)
    sql=f'SELECT chat_id FROM telebot WHERE user_name=(%s)'
    val=(user_name,)
    mycursor.execute(sql,val)
    res=mycursor.fetchall()[0][0]
    return res
def main_chat_id_getter_user_name(user_name):
    sql=f'SELECT chat_id FROM telebot WHERE user_name=(%s)'
    val=(user_name,)
    mycursor.execute(sql,val)
    res=mycursor.fetchall()[0][0]
    return res
def add_otp(chat_id,otp):
  sql=f'INSERT INTO otp_table VALUES(%s,%s)'
  val=(chat_id,otp)
  mycursor.execute(sql,val)
  mydb.commit()
def otp_getter(chat_id):
  sql=f'SELECT otp FROM otp_table WHERE chat_id=(%s)'
  chat_id=str(chat_id)
  val=(chat_id,)
  mycursor.execute(sql,val)
  res= mycursor.fetchall()[0][0]
  sql=f'DELETE FROM otp_table WHERE chat_id=(%s)'
  val=(chat_id,)
  mycursor.execute(sql,val)
  mydb.commit()
  return res
def gauth_deleter(chat_id):
  sql=f'DELETE FROM gauth WHERE chat_id=(%s)'
  val=(chat_id,)
  mycursor.execute(sql,val)
  mydb.commit()
def password_reset_table_inserter(msg,chat_id):
  sql=f'INSERT INTO reset_pass VALUES (%s,%s)'
  val=(msg,chat_id)
  mycursor.execute(sql,val)
  mydb.commit()
def password_reset_table_deleter(chat_id):
  sql=f'DELETE FROM reset_pass WHERE chat_id=(%s)'
  val=(chat_id,)
  mycursor.execute(sql,val)
  mydb.commit()
def password_reset_query(col_name,attribute,value):
  sql=f'SELECT {col_name} FROM reset_pass WHERE {attribute}=(%s)'
  val=(value,)
  mycursor.execute(sql,val)
  res=mycursor.fetchall()[0][0]
  return res
