import telebot
import random
import json
from telebot import types

answers = []
rightanswer = ''

def create_record(data, leviy_file):
    with open(leviy_file, 'w') as file:
        json.dump(data, file)

def read_record(filee):
    with open(filee, 'r') as file:
        data = json.load(file)
        return data

def update_record(filename, key, new_value):
    data = read_record(filename)
    data[key] = new_value
    create_record(data, filename)

data_read = read_record('voooprosi.json')

def randquest():
    que = random.choice(list(read_record('voooprosi.json').keys()))
    variants = data_read[que]
    ans = variants[0]
    random.shuffle(variants)
    return (que, variants, ans)

def nashsorted(el):
    return el['points']

def getquest(num, pl):
    num = str(num)
    global rightanswer, answers
    d = read_record('tekvop.json')
    question = d[num]['question']
    answers = d[num]['variants']
    rightanswer = d[num]['answer']
    keyplace = types.ReplyKeyboardMarkup(row_width=2)
    b1 = types.KeyboardButton(answers[0])
    b2 = types.KeyboardButton(answers[1])
    b3 = types.KeyboardButton(answers[2])
    b4 = types.KeyboardButton(answers[3])
    keyplace.add(b1, b2, b3, b4)
    bot.send_message(pl, f"{question}",
                     reply_markup=keyplace)


bot = telebot.TeleBot("6532443064:AAFUr22MiW64d8OMquxdqtVHyKs9tUMlgrc", parse_mode=None)

create_record({}, 'roomi.json')
create_record({}, 'tekvop.json')
create_record({}, 'players.json')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    keyplace = types.ReplyKeyboardMarkup()
    b1 = types.KeyboardButton('Сreate a room')
    b2 = types.KeyboardButton('Join a room')
    keyplace.add(b1, b2)
    bot.send_message(message.chat.id, "privet", reply_markup=keyplace)

@bot.message_handler(func=lambda message: message.text in answers)
def otvet(message):
    d = read_record('roomi.json')
    c = read_record('players.json')
    bivround = 0
    host = c[str(message.chat.id)]
    for t in d[str(host)]:
        if t['id'] == message.chat.id:
            bivround = t['round']
            t['round'] += 1
            if message.text == rightanswer:
                print('pravilno')
                t['points'] += 1
    print(d[str(host)])
    update_record('roomi.json', str(host),  d[str(host)])
    e = read_record('roomi.json')
    rounds = []
    for r in e[str(host)]:
        rounds.append(r['round'])
    rrr = rounds[0]
    truth = True
    for g in rounds:
        if rrr != g:
            truth = False
    if truth == False:
        bot.send_message(message.from_user.id, f"Вы ответили", reply_markup=types.ReplyKeyboardRemove())
        nuuuum = 0
        for r in e[str(host)]:
            if r['round'] != bivround:
                nuuuum += 1
        for f in e[str(host)]:
            bot.send_message(f['id'], f"Oтветили {nuuuum}/{len(rounds)}")
    elif truth ==  True:
        if rrr == 11:
            newlistt = sorted(e[str(host)], key=nashsorted)[::-1]
            for j in e[str(host)]:
                keyplace = types.ReplyKeyboardMarkup()
                b1 = types.KeyboardButton('/start')
                keyplace.add(b1)
                bot.send_message(j['id'], f"Вы набрали {j['points']}/10 баллов", reply_markup=types.ReplyKeyboardRemove())
                if len(newlistt) > 2:
                    bot.send_message(j['id'], f"Места:\n 🥇 {newlistt[0]['name']} : {newlistt[0]['points']} \n 🥈 {newlistt[1]['name']} : {newlistt[1]['points']} \n 🥉 {newlistt[2]['name']} : {newlistt[2]['points']}", reply_markup=types.ReplyKeyboardRemove())
                elif len(newlistt) == 2:
                    bot.send_message(j['id'], f"Места:\n 🥇 {newlistt[0]['name']} : {newlistt[0]['points']} \n 🥈 {newlistt[1]['name']} : {newlistt[1]['points']}", reply_markup=types.ReplyKeyboardRemove())
                bot.send_photo(j['id'], 'https://symbl-world.akamaized.net/i/webp/2e/0c6ff8789032ae9f484280fd98ac74.webp', reply_markup=keyplace)
            create_record({}, 'roomi.json')
            create_record({}, 'tekvop.json')
            create_record({}, 'players.json')
        else:
            bot.send_message(message.from_user.id, f"Вы ответили", reply_markup=types.ReplyKeyboardRemove())
            for i in e[str(host)]:
                bot.send_message(i['id'], f"Oтветили {len(rounds)}/{len(rounds)}, следующий вопрос:",
                                 reply_markup=types.ReplyKeyboardRemove())
                getquest(rrr, i['id'])


@bot.message_handler(content_types=['text'])
def phrasess(message):
    if message.text == 'Сreate a room':
        keyplacee = types.ReplyKeyboardMarkup()
        b1 = types.KeyboardButton('START')
        keyplacee.add(b1)
        bot.send_message(message.chat.id, f"Your room: {message.chat.id}. You can press 'START' when the players connect", reply_markup=keyplacee)
        update_record('roomi.json',  message.chat.id, [{'id': message.chat.id, 'name' : message.from_user.first_name, 'points' : 0, 'round' : 1}])
    if message.text == 'Join a room':
        if len(read_record('roomi.json')) == 0:
            bot.send_message(message.chat.id, "There's no created rooms yet(")
        else:
            keyplace1 = types.ReplyKeyboardMarkup()
            for i in read_record('roomi.json'):
                b1 = types.KeyboardButton(i)
                keyplace1.add(b1)
            bot.send_message(message.chat.id, f"Select a room", reply_markup=keyplace1)
    if message.text in read_record('roomi.json'):
        naammee = message.from_user.first_name
        diii = read_record('roomi.json')
        lii = list(diii[message.text])
        lii.append({'id': message.chat.id, 'name' : message.from_user.first_name, 'points' : 0, 'round' : 1})
        update_record('roomi.json', message.text, lii)
        bot.send_message(message.chat.id, f"You've joined the room", reply_markup=types.ReplyKeyboardRemove())
        lll = read_record('roomi.json')
        for i in lll[message.text]:
            ids = i['id']
            bot.send_message(ids, f"{naammee} joined the room")
    if message.text == 'START':
        for i in range(1, 11):
            qu, var, an = randquest()
            update_record('tekvop.json', i, {'question' : qu, 'variants' : var, 'answer' : an})
        pllist = []
        llll = read_record('roomi.json')
        for i in llll[str(message.chat.id)]:
            ids = i['id']
            pllist.append(ids)
        ppll = {}
        for s in pllist:
            update_record('players.json', s, message.chat.id)
            getquest('1', s)




bot.polling(none_stop=True, interval=0)