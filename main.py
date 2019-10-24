import telebot
import os, pickle
import requests
import bs4
from urls import *

from PyMailCloud import PyMailCloud
from PyMailCloud import PyMailCloudError
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#mail_cloud = PyMailCloud("ejudgetest@mail.ru", "00ejudge00")

bot = telebot.TeleBot('853967300:AAFlW9k5u-RcKnkRgIka9zAcmnlV-PkAwK4')
data = {
    
}

kb = telebot.types.ReplyKeyboardMarkup()
kb.row('/update')

#os.remove("users.pkl")
#mail_cloud.download_files("/users.pkl")

with open("users.pkl", "rb") as f:
    data = pickle.load(f)

def dump():
    with open('users.pkl', 'wb') as f:
        pickle.dump(data, f)
    mail_cloud.delete_files([{'filename' : 'users.pkl'}])
    mail_cloud.upload_files([{'filename' : 'users.pkl', 'path' : '/'}])

@bot.message_handler(commands=['start'])
def hello_msg(msg):
    bot.send_message(msg.chat.id, cmd)

@bot.message_handler(commands=['contestid'])
def id_msg(msg):
    ans = ""
    for i in range(len(contests)):
        ans += str(i) + " " + contests[i] + "\n"
    bot.send_message(msg.chat.id, ans)

@bot.message_handler(commands=['update'])
def upd(msg):
    #print(data)
    ans = ""
    for i in range(len(contests)):
        if contests[i] not in data:
            data[contests[i]] = {}
            bot.send_message(my_id, "Новый контест - " + contests[i])
    for i in range(len(contests)):
        #print(data)
        #if (contests)
        r = requests.get(urls[i])
        r.encoding = 'utf-8'
        b = bs4.BeautifulSoup(r.text, features='lxml')
        table = b.find_all('table')[1]
        tasks = table.find_all('tr')
        for row in tasks[1:len(tasks)-3]:
            res = []
            row = row.find_all('td')
            name = row[1].get_text()
            if (name not in data[contests[i]]):
                data[contests[i]][name] = ['0']*(len(row) - 4)
                bot.send_message(my_id, contests[i] + "\nНовый юзер - " + name) 
           # print(data)
            for cell in row[2:len(row) - 2]:
                c = cell.get_text()
                if (c[0] == '+'):
                    res.append(c)
                else:
                    if ('cell_attr_pr' in cell['class']):
                        res.append('?' + c[1:])
                    elif c[0] == '-':
                        res.append(c)
                    else:
                        res.append('0')
            resp = ""
           # print(data[contests[i]][name], len(res))
            for j in range(len(res)):
                if (data[contests[i]][name][j] != res[j]):
                    resp += str(chr(ord('A') + j)) + ". " + data[contests[i]][name][j] + " -----> " + res[j] + "\n"
                    data[contests[i]][name][j] = res[j]
            if (len(resp) > 0):
                bot.send_message(my_id, contests[i] + " " + name + "\n" + resp)
    #dump()
    bot.send_message(my_id, "Больше обновлений нет", reply_markup=kb)

bot.polling()