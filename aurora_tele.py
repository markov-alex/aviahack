import telebot
import requests
import json

from telebot import types


namef = 'citiesRus.txt'
def NameCities(namef):
    f = open(namef, 'r')
    count = 0
    key = ''
    dictCities = {}
    for i in f:
        if count % 2 == 0:
            i = i.strip()
            key = i.lower()
            count += 1
        else:
            i = i.strip()
            dictCities[key] = i
            count += 1
    return(dictCities)

def Rezult(city):
    if city.lower() in NameCities(namef):
        return NameCities(namef)[city.lower()]

def data_save(OUT_, IN_, years, month, id_):
    print('fgh')
    token = 'd20970f1ea95552694cd7347c8c11d29'
    OUT_ = Rezult(OUT_)
    IN_ = Rezult(IN_)
    if OUT_ == None or IN_ == None:
        bot.send_message(id_, f"Вы ввели неправильные данные")
        return
    flag = 0
    response = requests.get(f"http://api.travelpayouts.com/v1/prices/calendar?depart_date={years}-{month}&origin={OUT_}&destination={IN_}&token={token}")
    response = json.loads(response.text)
    for data_1 in response['data']:
        data_= response['data'][data_1]
        if data_['airline'] == 'HZ' or data_['airline'] == 'SU':
            flag = 1
            bot.send_message(id_, f"Рейс = {data_['flight_number']}\n"
                        f"Цена билета: {data_['price']}руб. \n"
                        f"Откуда: {data_['origin']} \n"
                        f"Куда: {data_['destination']} \n"
                        f"Время и дата вылета: {data_['departure_at']} \n"
                        f"Время прибытия: {data_['return_at']} \n"
                   f"Авиакомпания: {data_['airline']}")
    if flag == 0:
        bot.send_message(id_, f"ближайших рейсов нет")
        return




import app.db.struct__ as x
#-------Links------------
constLink='http://aviahack.varanga-studio.com/'
LinkAurora='https://www.flyaurora.ru/buy/services/'
tokenMy="694597674:AAHStgCMApDVJmixUt9CXpYMcE8MZ2wi2cY"
bot = telebot.TeleBot(tokenMy)
helpFrase='Я всегда рада помочь'
#-------Butoms---------------
@bot.message_handler(commands=['help'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup()
    keyboard1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    keyboard1.row("/menu")
    bot.send_message(message.chat.id, "Выберите интересующую категорию"
                                        ' В начало /menu', reply_markup=markup)



@bot.message_handler(commands=['start','menu'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('/Расписание')
    markup.row('/Правила перевозок')
    markup.row('/Бронирование перевозок')
    markup.row('/Операции с бронированием')
    markup.row('/Проверка наличие мест')
    bot.send_message(message.chat.id, "Я Аврора-бот, чем я могу быть полезен?", reply_markup=markup)

@bot.message_handler(commands=['Расписание'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Откуда вылет?",reply_markup=markup)
    bot.register_next_step_handler(msg, getDepartment)



def getDepartment(message):
        pasInf = x.PasssangerInfo(message.chat.id)
        pasInf.department = message.text
        pasInf.department=pasInf.department.lower()
        print((pasInf.department))
        msg = bot.send_message(message.chat.id, "Куда летит?")
        bot.register_next_step_handler(msg, getArrive)


def getArrive(message):
    pasInf = x.PasssangerInfo(message.chat.id)
    pasInf.arrive = message.text
    pasInf.arrive = pasInf.arrive.lower()
    msg = bot.send_message(message.chat.id, "Когда летит?")
    bot.register_next_step_handler(msg,getDateBook)


def getDateBook(message):
    pasInf = x.PasssangerInfo(message.chat.id)
    data = message.text.split()
    pasInf.year=data[0]
    pasInf.month=data[1]
    print(pasInf.month)
    print(pasInf.year)
    data_save(pasInf.department,pasInf.arrive,pasInf.year,pasInf.month,message.chat.id,)


@bot.message_handler(commands=['Правила','назад'])
def handle_start(message):
    #print("I Правила перевозок")
    markup = types.ReplyKeyboardMarkup()
    markup.row('/Нормы багажа')
    markup.row('/Габаритные вещи')
    markup.row('/Домашние животные')
    markup.row('/Спортивный инвентарь')
    markup.row('/menu')
    bot.send_message(message.chat.id, "Выберите нужную категорию", reply_markup=markup)


@bot.message_handler(commands=['Нормы'])
def handle_start(message):
    #print("I Правила перевозок")
    markup = types.ReplyKeyboardMarkup()
    markup.row('/Внутрирегиональные')
    markup.row('/Межрегиональные')
    markup.row('/Международные')
    bot.send_message(message.chat.id, "Выберите нужную категорию", reply_markup=markup)


@bot.message_handler(commands=['Международные','Межрегиональные'])
def handle_start(message):
    #print("I Правила перевозок")
    markup = types.ReplyKeyboardMarkup()
    markup.row('/Аэрофлот')
    markup.row('/Аврора')
    bot.send_message(message.chat.id, "Выберите нужную категорию", reply_markup=markup)

@bot.message_handler(commands=['Аэрофлот'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, get_data2('norm',1), reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    m1 = types.KeyboardButton('/назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


@bot.message_handler(commands=['Аврора'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, get_data2('norm',2), reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


@bot.message_handler(commands=['Внутрирегиональные'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, get_data2('norm',0), reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)



@bot.message_handler(commands=['Габаритные'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "В разработке", reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


@bot.message_handler(commands=['Домашние','Назад'])
def handle_start(message):
    #print("I Правила перевозок")
    markup = types.ReplyKeyboardMarkup(row_width=0.5, resize_keyboard=True)
    markup.row('/Салон','/Багаж')
    markup.row('/Воздушный отсек','/Вес >=50')
    markup.row('/Собаки проводники','/Оплата')
    markup.row('/Документы','/Доп. инфо')
    markup.row('/назад','/menu')
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup)

@bot.message_handler(commands=['Салон'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, get_data2('animals',0), reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/Назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


@bot.message_handler(commands=['Багаж'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, get_data2('animals',1),
                     reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/Назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)

@bot.message_handler(commands=['Воздушный'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, get_data2('animals',2),
                     reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/Назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


@bot.message_handler(commands=['Собаки'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, get_data2('animals',3),
                     reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/Назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


@bot.message_handler(commands=['Вес'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, get_data2('animals',4),
                     reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/Назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


@bot.message_handler(commands=['Оплата'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, get_data2('animals',5),
                     reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/Назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


@bot.message_handler(commands=['Документы'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, get_data2('animals',6),
                     reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/Назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)

@bot.message_handler(commands=['Доп.'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id,  get_data2('animals',7),
                     reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/Назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


@bot.message_handler(commands=["Спортивный"])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, "В разработке", reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/назад')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)

@bot.message_handler(commands=['Бронирование'])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    msg = bot.send_message(message.chat.id, "Откуда вылет?",reply_markup=markup)
    bot.register_next_step_handler(msg, getDepartmentBook)

def getDepartmentBook(message):
        pasInf = x.PasssangerInfo(message.chat.id)
        pasInf.department = message.text
        pasInf.department = pasInf.department.lower()
        print((pasInf.department))
        msg = bot.send_message(message.chat.id, "Куда летит?")
        bot.register_next_step_handler(msg, getArriveBook)


def getArriveBook(message):
    pasInf = x.PasssangerInfo(message.chat.id)
    pasInf.arrive = message.text
    pasInf.arrive = pasInf.department.lower()
    print((pasInf.arrive))
    msg = bot.send_message(message.chat.id, "Дата вылета ГГГГ MM?")
    bot.register_next_step_handler(msg, getDateBook)


# def getDateBook(message):
#     pasInf = x.PasssangerInfo(message.chat.id)
#
#     data = message.text.split()
#     pasInf.year=data[0]
#     pasInf.month=data[1]
#     print(pasInf.month)
#     print(pasInf.year)
#     data_save(pasInf.department,pasInf.arrive,pasInf.year,pasInf.month,message.chat.id,)




@bot.message_handler(commands=["Операции"])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id,  f"Перейдите по ссылке\n{LinkAurora}", reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/menu')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


@bot.message_handler(commands=["Проверка"])
def handle_start(message):
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, f"Перейдите по ссылке\n{LinkAurora}"
                                        , reply_markup=markup)
    markup1 = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    m1 = types.KeyboardButton('/menu')
    markup1.add(m1)
    bot.send_message(message.chat.id, helpFrase, reply_markup=markup1)


#--------------host-----------------------------------------------------


def get_data(from_, to_):
    response = requests.get(constLink+'schedule?from='+from_+'&to='+to_)
    response = json.loads(response.text)
    return response

def get_data2(object_, id):
        response = requests.get(constLink+str(object_)+'?normType='+str(id))
        a = json.loads(response.text)
        return a['result']



bot.polling(none_stop=True, interval=0)
