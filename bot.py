import telebot
import requests
import random
import json
from telebot import types
import sender
import main
import urllib
import doc

#-------Links------------
tokenMy='1746118771:AAEvKJ4e-OzGwNXdo7rhwatp37pD1GMnJu4'
bot = telebot.TeleBot(tokenMy)
helpFrase='Я всегда рад помочь'
send='docAvia'
img_id=None
phone=None
img_name_tmp='tmp.png'
reg=None
personal_info={}
file_send_mail=None
def msg_sms():
	chislo=random.randrange(1000, 9999)
	return str(chislo)

#-------Butoms---------------
@bot.message_handler(commands=['help'])
def handle_start(message):
    print('hello  help')
    bot.send_message(message.chat.id, helpFrase)


@bot.message_handler(commands=['start'])
def handle_start(message):
    markup =telebot.types.ReplyKeyboardMarkup(True)
    markup.row('/Войти в кабинет')
    markup.row('/Регистрация')
    markup.row('/help')
    bot.send_message(message.chat.id, 'Здравствуй!\n\n Я твой виртуальный ассистент в заполнении и подписании документов\nДавай начнем!', reply_markup=markup)

@bot.message_handler(commands=['Регистрация'])
def handle_start(message):
    markup =telebot.types.ReplyKeyboardMarkup(True)
    markup.row('/start')
    msg=bot.send_message(message.chat.id, 'Введите свое ФИО(Иванов Иван Иванович) через пробел', reply_markup=markup)
    if message.text!='/start':
        bot.register_next_step_handler(msg, reg_name)


def reg_name(message):
    global reg
    reg=True
    fio=message.text.split(' ')
    global personal_info
    personal_info['surname']=fio[0]
    personal_info['name']=fio[1]
    personal_info['otch']=fio[2]
    msg=bot.send_message(message.chat.id, 'Введите дату рождения через пробел(26 04 2021)')
    bot.register_next_step_handler(msg,reg_date)

def reg_date(message):
    date_l=message.text.split(' ')
    date=date_l[2]+'-'+date_l[1]+'-'+date_l[0]
    print(date)
    global personal_info
    personal_info['date']=date
    markup1 =telebot.types.ReplyKeyboardMarkup(True, True)
    phone= types.KeyboardButton(text="Добавить телефон", request_contact=True) #Указываем название кнопки, которая появится у пользователя
    markup1.add(phone)
    bot.send_message(message.chat.id,'Дообавьте телефон' , reply_markup=markup1)



@bot.message_handler(commands=['Войти'])
def handle_start(message):
    markup1 =telebot.types.ReplyKeyboardMarkup(True, True)
    phone= types.KeyboardButton(text="Отправить телефон", request_contact=True) #Указываем название кнопки, которая появится у пользователя
    markup1.add(phone)
    bot.send_message(message.chat.id,'Подтвердите' , reply_markup=markup1)

@bot.message_handler(content_types=['contact']) #Объявили ветку, в которой прописываем логику на тот случай, если пользователь решит прислать номер телефона :) 
def contact(message):
    if message.contact is not None:
        global phone
        phone='+'+message.contact.phone_number
        if main.man_in_table('8'+phone[2:]):
            
            msg=bot.send_message(message.chat.id,'Введите номер из сообщения')
            global code
            code=msg_sms()
            #main.smsc.send_sms(phone, code, sender=send)
            bot.register_next_step_handler(msg, check)
        else:
            markup1 =telebot.types.ReplyKeyboardMarkup(True, True)
            markup1.row('/start')
            bot.send_message(message.chat.id,'Зарегистрируйтесь',reply_markup=markup1)

        


def check(message):
    print(code)
    global reg,personal_info,phone
    markup1 =telebot.types.ReplyKeyboardMarkup(True, True)
    print(message.text)
    if message.text=='1111':
        if reg==None:
            markup1.row('/Готово')
            bot.send_message(message.chat.id,'Все верно' , reply_markup=markup1)
        else:
            personal_info['phone']='8'+phone[2:]
            print(personal_info)
            main.insert_human_table(personal_info['name'],personal_info['surname'],personal_info['otch'],personal_info['date'],personal_info['phone'])
            print(main.man_in_table('8'+phone[2:]))
            markup1.row('/Готово')
            bot.send_message(message.chat.id,'Все верно' , reply_markup=markup1)
    else:
        markup1.row('/start')
        markup1.row('/Отправить еще раз')
        bot.send_message(message.chat.id,'Неверный код' , reply_markup=markup1)


@bot.message_handler(commands=['Отправить']) #Объявили ветку, в которой прописываем логику на тот случай, если пользователь решит прислать номер телефона :) 
def handle_start(message):
    msg=bot.send_message(message.chat.id,'Введите номер сообщения')
    code=msg_sms()
    main.smsc.send_sms(phone, code, sender=send)
    bot.register_next_step_handler(msg, check)

@bot.message_handler(commands=['Готово','menu']) 
def handle_start(message):
    global phone
    print(phone)
    markup =telebot.types.ReplyKeyboardMarkup(True,True)
    #markup.row('/Моя подпись')
    markup.row('/Список обазцов документов')
    bot.send_message(message.chat.id,'Добро пожаловать в личный кабинет!\n\n Есть вопросы напиши /info' , reply_markup=markup)

@bot.message_handler(commands=['Мои']) 
def handle_start(message):
    global phone
    print(phone)
    markup =telebot.types.ReplyKeyboardMarkup(True)
    markup.row('/menu')

@bot.message_handler(commands=['Моя']) 
def handle_start(message):
    global phone
    print(phone)
    markup =telebot.types.ReplyKeyboardMarkup(True,True)
    markup.row('/Просмотреть подпись')
    markup.row('/Создать подпись')
    markup.row('/menu')
    bot.send_message(message.chat.id,'Выберете категорию' , reply_markup=markup)


@bot.message_handler(commands=['Создать']) 
def handle_start(message):
    print('hello sign')
    global phone

    #link='http://redpix8i.beget.tech/images/6084448d122b6.png'
    markup=telebot.types.InlineKeyboardMarkup()
    markup1=telebot.types.ReplyKeyboardMarkup(True)

    global img_id
    #if img_id==None:
    phone='8'+phone[2:]
    phone_dict={'phone': phone}
    text=message.text[31:]
    print(phone_dict)
    r = requests.get('http://redpix8i.beget.tech/', params=phone_dict)
    print(r.url)
    url_but=types.InlineKeyboardButton(text="Получить подпись", url=r.url,callback_data='Получить подпись')
    markup.add(url_but)
    m=bot.send_message(message.chat.id,'Перейдите по ссылке и создайте подпись' , reply_markup=markup)
    print(message.date)
    if message.date==r.url:
        img_id=True
        markup1.row(f'/Подписать обращение {text}')
        markup1.row('/menu')
        bot.send_message(message.chat.id,'Нажимая кнопку подписать Вы получаете готовое обращение с Вашими персональными данными и электронной пописью ' , reply_markup=markup1)
    # else:
    #     urllib.request.urlretrieve(f"http://redpix8i.beget.tech/images/{phone}.png", "tmp1.png")
    #     bot.send_message(message.chat.id,'У Вас уже есть подпись' , reply_markup=markup1)
    #     bot.send_photo(message.chat.id,open("tmp1.png",'rb'))



@bot.message_handler(commands=['Просмотреть']) 
def handle_start(message):
    global phone, img_id
    markup1=telebot.types.ReplyKeyboardMarkup(True)
    markup1.row('/menu')
    if img_id==None:
        bot.send_message(message.chat.id,'У вас нет подписи' , reply_markup=markup1)
        
    else:
        urllib.request.urlretrieve(f"http://redpix8i.beget.tech/images/{phone}.png", "tmp1.png")
        bot.send_message(message.chat.id,'Ваша подпись' , reply_markup=markup1)
        bot.send_photo(message.chat.id,open("tmp1.png",'rb'))
    
    
@bot.message_handler(commands=['Список']) 
def handle_start(message):
    markup =telebot.types.ReplyKeyboardMarkup(True,True)
    markup.row('/Потеря имущества')
    markup.row('/Оформление вип зала')
    markup.row('/Возврат билета')
    markup.row('/menu')
    bot.send_message(message.chat.id,'Вы можете выбрать интересующий Вас образец документа' , reply_markup=markup)
    

@bot.message_handler(commands=['Потеря','Оформление','Возврат']) 
def handle_start(message):
    markup =telebot.types.ReplyKeyboardMarkup(True,True)
    print(message.text)
    global img_id
    # img_id!=None:
    markup.row(f'/Создать подпись для обращение {message.text[1:].lower()}')
        #markup.row(f'/Подписать обращение {message.text[1:].lower()}')
    markup.row('/menu')
    bot.send_message(message.chat.id,'Вы создаете свою подпись для данного документа' , reply_markup=markup)
        #bot.send_message(message.chat.id,'Нажимая кнопку подписать Вы получаете готовое обращение с Вашими персональными данными и электронной пописью ' , reply_markup=markup)
    # else:
    #     markup.row('/menu')
    #     bot.send_message(message.chat.id,'У вас нет подписи создайте ее вначале' , reply_markup=markup)


@bot.message_handler(commands=['Подписать']) 
def handle_start(message):
    markup =telebot.types.ReplyKeyboardMarkup(True,True)
    print(message.text)
    global phone
    print(phone)
    markup.row('/menu')
    print(f'тип-{message.text[21:].strip()}')
    link=doc.change_doc(message.text[21:].strip(),phone)
    file_1=open(link,'rb')
    bot.send_document(message.chat.id,file_1, reply_markup=markup)
    file_1.close
    msg=bot.send_message(message.chat.id,'Данный документ можете отправить на Вашу почу\n\n Введите её:' , reply_markup=markup)
    if message.text!='/menu':
        bot.register_next_step_handler(msg, mail)



def mail(message):
    subject='Обращение'
    text='Вам пришло обращение подписанной в AviaBot'
    print([message.text])
    sender.send_files([message.text],subject,text,['tmp.docx'])



bot.polling()
