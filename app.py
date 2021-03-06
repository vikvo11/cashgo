import pymongo
from pymongo import MongoClient
import json
import pymongo
from bson import BSON
from bson import json_util
from flask import Flask, flash, redirect, render_template, request, session, abort,url_for,logging #For work with HTTP and templates
import requests # For HTTP requests
from functools import wraps # For lock access
from HTTP_basic_Auth import auths # For lock access
from flask_mysqldb import MySQL #For connect to MySQL DB

from flask import jsonify #For response in /webhook
from flask_sslify import SSLify #For use HTTPS
from misck import token,chat_id_old # Misck.py - config for telegram_bot
from flask import make_response
import re
import telebot
from telebot import types



#********
#import socket
#import socks
#socks.set_default_proxy(socks.SOCKS5, '148.251.130.165',8080,True)
#socket.socket = socks.socksocket
#print(requests.get('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/setWebhook?url=').text)
#print(requests.get('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/setWebhook?url=https://vorovik.pythonanywhere.com/webhooks/').text)
#answer = {'chat_id': 488735610, 'text': 'test'}
#print(requests.post('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/sendMessage',data=answer).text)
#*********

#select from costs ;
#delete from costs where id=25;
URL='https://api.telegram.org/bot{}/'.format(token)
app = Flask(__name__)
app.config['SECRET_KEY'] = 'morkovka18'
app.debug = True
sslify=SSLify(app)
#Config mysql
app.config['MYSQL_HOST']='vorovik.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER']='vorovik'
app.config['MYSQL_PASSWORD']='cb.,fq12-'
app.config['MYSQL_DB']='vorovik$vorovikapp'
app.config['MYSQL_CURSORCLASS']='DictCursor'
#init MySQL
mysql=MySQL(app)

#*****
global last_msg
last_msg=''

curs =3 # 1=RUB; 3=CZK
currency = 'CZK' # 'RUB'
limit_value='limit_czk_value' #'limit_value' - RUB


#https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/setWebhook?url=https://vorovik.pythonanywhere.com/webhooks/

#*****
bot = telebot.TeleBot(token)
key_default = types.ReplyKeyboardMarkup(resize_keyboard=True)
key_default.row(types.KeyboardButton('Button 1'))
key_default.row(types.KeyboardButton('Button 2'))
key_default.row(types.KeyboardButton('Button 3'))

@bot.message_handler(content_types=["text"])
def default_test(message):
    keyboard = types.InlineKeyboardMarkup()
    url_button = types.InlineKeyboardButton(text="Перейти на Яндекс", url="https://ya.ru")
    keyboard.add(url_button)
    bot.send_message(message.chat.id, "Привет! Нажми на кнопку и перейди в поисковик.", reply_markup=keyboard)

@bot.message_handler(func=lambda message: messages.text == u'Button 1') #Если была вызвана Button 1
#Тут пишем метод который будет выполнятся, когда нажмём на кнопку
def button(message):
    #send_message(chat_id,parc_text(text))
     bot.send_message(chat_id_old, 'Сюда пишем текст типо - Привет')
#*****

def write_json(data,filename='answer.json'):
    with open(filename,'w') as f:
        json.dump(data,f,indent=2,ensure_ascii=False)


def get_updates():
    url=URL+'getUpdates'
    r=requests.get(url)
    write_json(r.json())
    return r.json()

def send_message(chatId,text='Please wait a few seconds...!'):
    url=URL+'sendMessage'
    answer = {'chat_id': chatId, 'text': text}
    print(answer)
    #r=requests.get(url,json=answer)
    #print(r.json())

    request = requests.post(url, data=answer)

    print(request.json())
    return request.json()

def parc_text(text):
    # bitcoin pattern = r'/\w+'
    pattern =r'/\S+'
    crypto = re.search(pattern,text).group()
    return crypto[1:]
#patter1=r' \w+'
#k=re.search(pattern,text)
#kk=re.search(pattern,k)
def parc_text_cost(text):
    #pattern = r' \w+'
    pattern = r' \-?[0-9]\d*(\.\d+)?$'
    cost = re.search(pattern,text).group()
    return cost[1:]

def get_price(crypto):
    url='https://api.coinmarketcap.com/v1/ticker/{}/'.format(crypto)
    r = requests.get(url).json()
    price = r[-1]['price_usd']
    return price

#Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args,**kwargs):
        if 'logged_in' in session:
            return f(*args,**kwargs)
        else:
            #flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@is_logged_in
def home():
    a=1
    return redirect(url_for('dashbord'))


#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out','success')
    return redirect(url_for('login'))

#User Login
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #Get Form fields
        username = request.form['username']
        password_candidate = request.form['password']
        #users=auths()
        if auths(username,password_candidate):
            session['logged_in']= True
            return redirect(url_for('dashbord'))
        else:
                error='Invalid login'
                return render_template('login.html',error=error)

    return render_template('login.html')

#Dashbord
@app.route('/dashbord',methods=['GET','POST'])
@is_logged_in
def dashbord():
    #msg = py()
    #add_costs('costs','test123',100)
    #table='costs'
    #title='test'
    #cost=100
    #update_costs('costs','test123',100)
    msg = mysqls('costs')
    #keys = dict(msg[0])
    #b=msg.keys()
    return render_template('dashbordpymongo.html', articles=msg)

#Articles
@app.route('/articles')
def articles():
    # Create cursor
    cur = mysql.connection.cursor()

    # Get articles
    result = cur.execute("SELECT * FROM articles")

    articles = cur.fetchall()

    if result > 0:
        return render_template('articles.html', articles=articles)
    else:
        msg = 'No Articles Found'
        return render_template('articles.html', msg=msg)
    # Close connection
    cur.close()

@app.route('/webhooks/',methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        r = request.get_json()
        chat_id=r['message']['chat']['id']
        text=r['message']['text']
        global last_msg
        last_msg=json.dumps(r,ensure_ascii=False)
        #bitcoin pattern =r'/\w+'
        pattern =r'/\S+'
        patternSum =r'/сумма'
        patternLim =r'/лимит'

        #answer = {'chat_id': 488735610, 'text': 'test'}
        #print(requests.post('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/sendMessage',data=answer).text)
        if re.search(patternLim,text):
            cur = mysql.connection.cursor()
            Lims=cur.execute("SELECT title,limits,cost FROM costs where year=(Select Year(CURDATE())) and month=(select month(CURDATE())) and title !=%s",['кредит'])
            Lims = cur.fetchall()
            cur.close()
            #send_message(chat_id,'Категория = '+str(Lim['title'])+'лимит=' + str(Lim['limits']))
            for Lim in Lims:
                #send_message(chat_id,'Категория = '+str(Lim['title'])+' лимит=' + str(Lim['limits']))
                #send_message(chat_id,str(Lim['title'])+' текущий = '+str(Lim['cost']) +' лимит=' + str(Lim['limits']))
                #limmsg=limmsg+str(Lim['title'])+' текущий = '+str(Lim['cost']) +' лимит=' + str(Lim['limits'])
                limmsg=str(Lim['title'])+': текущий = '+str(Lim['cost']) +currency+' лимит=' + str(Lim['limits'])+currency
                #lmsg=lmsg+""+limmsg+". \n"
            send_message(chat_id,""+limmsg+". \n"+limmsg+"")

            return jsonify(r)

        if re.search(patternSum,text):
            cur = mysql.connection.cursor()
            Sum=cur.execute("SELECT sum(cost) as summa FROM costs where year=(Select Year(CURDATE())) and month=(select month(CURDATE())) and title !=%s",['кредит'])
            Sum = cur.fetchone()
            cur.close()
            send_message(chat_id,'Общая потраченная сумма в этом месяце = '+str(Sum['summa']))
            return jsonify(r)
        else:
            if re.search(pattern,text) and not re.search(patternLim,text) :
                #bitcoin price = get_price(parc_text(text))
                cost=parc_text_cost(text)
                cost.replace(" ", "")

            #add_costs()
            #send_message(chat_id,price)
            #add_costs('costs','test123',100)

            #*update_costs('costs',str(parc_text(text)),int(cost))

            #current_costs('costs',str(parc_text(text)))

            #*send_message(chat_id,parc_text(text))
                send_message(chat_id,update_costs('costs',str(parc_text(text)),int(cost)))
            #update_costs('costs','test123',100)
            #if re.search(pattern1,text):
                #a=re.search(pattern1,text)
                #update_costs('costs',a,900)
            return jsonify(r)

    return '<h1>Hello bot</h1>'

@app.route('/webhooks1/',methods=['POST','GET'])
def webhooks1():
    if request.method == 'GET':
        #socks.set_default_proxy(socks.SOCKS5, '148.251.130.165',8080,True)
        #socket.socket = socks.socksocket
        answer1 = {'chat_id': 488735610, 'text': 'test'}
        #requests.post('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/sendMessage',data=answer1).text
        #requests.post('https://yandex.ru',data=answer1)
        requests.post('https://api.telegram.org/bot521265983:AAFUSq8QQzLUURwmCgXeBCjhRThRvf9YVM0/sendMessage',data=answer1)
        return '<h1>Hello bot</h1>'

    return '<h1>Hello bot</h1>'

@app.route('/last_msg/',methods=['POST','GET'])
#curl -u vorovik:python123 -i https://vorovik.pythonanywhere.com/last_msg/
def teslast():
    r='<h2>{}</h2>'.format(str(last_msg))
    return r

def py():
    client = MongoClient("ds141786.mlab.com:41786", username = 'podarkin', password = 'podarkin', authSource = 'heroku_q51pzrtm')
    db = client["heroku_q51pzrtm"]
    bookings_coll = db.bookings
    doc = bookings_coll.find_one()
    asa = json.dumps(doc, sort_keys=True, indent=4, default=json_util.default)
    docs = bookings_coll.find()
    id = docs[0]['name']
    return docs
def mysqls(table):
    # Create cursor
    cur = mysql.connection.cursor()
    # Get articles
    #result = cur.execute("SELECT * FROM %s",(art))
    #result = cur.execute("SELECT * FROM articles")
    result = cur.execute("SELECT * FROM {}".format(table))

    #result = cur.execute("SELECT * FROM users WHERE username=%s",[username])
    #cur.execute("INSERT INTO articles(title,author,body) VALUES(%s,%s,%s)",(title,session['username'],body))
    articles = cur.fetchall()
    cur.close()
    return articles

def add_costs(table,title,cost):
    #Create cursor
    cur = mysql.connection.cursor()
    #Execute query
    #cur.execute("INSERT INTO {}(title,cost,year,month) VALUES(%s,%s,(Select Year(CURDATE())),(select month(CURDATE())))".format(table),(title,cost))
    cur.execute("INSERT INTO {}(title,cost,year,month) VALUES(%s,%s,(Select Year(CURDATE())),(select month(CURDATE())))".format(table),(title,cost))
    #result = cur.execute("SELECT * FROM {} WHERE id=%s".format('articles'),[username])
    #Commit ot db
    mysql.connection.commit()
    #Close connection
    cur.close()
    return 'ok'

def update_costs(table,title,cost):
    #Create cursor
    cur = mysql.connection.cursor()
    #Execute query
    #year and month
    result = cur.execute("SELECT * FROM {} where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),[title])
    limit= cur.execute("SELECT * FROM limit_dict where title=%s",[title])
    if result>0:
        if limit>0:
            cur.execute("UPDATE {} SET cost=cost+%s,limits=limits-%s where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),(cost,cost,title))
        else:
            cur.execute("UPDATE {} SET cost=cost+%s where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),(cost,title))
        #cur.execute("UPDATE {} SET cost=cost+%s where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),(cost,title))
        mysql.connection.commit()
        result = cur.execute("SELECT * FROM {} where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),[title])
        result = cur.fetchone()
        #cur.close()
    else:
        if limit>0:
            limits= cur.execute("SELECT * FROM limit_dict where title=%s",[title])
            limits = cur.fetchone()
            cur.execute("INSERT INTO {}(title,cost,year,month,limits) VALUES(%s,%s,(Select Year(CURDATE())),(select month(CURDATE())),%s)".format(table),(title,cost,int(limits[str(limit_value)])-cost))
        else:
            cur.execute("INSERT INTO {}(title,cost,year,month) VALUES(%s,%s,(Select Year(CURDATE())),(select month(CURDATE())))".format(table),(title,cost))
        #cur.execute("INSERT INTO {}(title,cost,year,month) VALUES(%s,%s,(Select Year(CURDATE())),(select month(CURDATE())))".format(table),(title,cost))
        #result = cur.execute("SELECT * FROM {} WHERE id=%s".format('articles'),[username])
        #Commit ot db
        mysql.connection.commit()
        result = cur.execute("SELECT * FROM {} where title=%s and year=(Select Year(CURDATE())) and month=(select month(CURDATE()))".format(table),[title])
        result = cur.fetchone()

        #Close connection
        #cur.close()
    #return str(result)
    #limit= cur.execute("SELECT * FROM limit where title=%s",[title])
    if limit>0:
        limits= cur.execute("SELECT * FROM limit_dict where title=%s",[title])
        limits = cur.fetchone()

        LimitSum= cur.execute("SELECT * FROM limit_dict where title=%s",['общий'])
        limitsSum = cur.fetchone()
        Sum=cur.execute("SELECT sum(cost) as summa FROM costs where year=(Select Year(CURDATE())) and month=(select month(CURDATE())) and title !=%s",['кредит'])
        Sum = cur.fetchone()
        testsum=str(limitsSum[str(limit_value)]-Sum['summa'])
        if int(testsum)<10000/curs:
            totallimit='Заканчивается общий лимит!!! Осталось ='+testsum+' '+currency
        else:
            totallimit=''
        cur.close()
        return ('Затраты в текущем месяце на '+str(result['title'])+'= '+str(result['cost'])+' '+currency+'. Лимит = '+str(result['limits'])+' '+currency+' '+totallimit)
    else:
        cur.close()
        return ('Затраты в текущем месяце на '+str(result['title'])+'= '+str(result['cost'])+' '+currency)
def main():
    #doc = bookings_coll.find_one()


    pass
   # a = [x for x in bookings_coll.find()]


if __name__ == '__main__':
    #bot.polling(none_stop=True)
    main()
