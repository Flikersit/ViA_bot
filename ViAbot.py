import telebot 
from telebot import types
import webbrowser
import os

import config 

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)


bot = telebot.TeleBot(config.API_TOKEN)

language = 0

i = 0


buttons_language = {
                'button1':['тавары', 'products', 'товары'], 
                'button2':['налады', 'settings', 'настройки'], 
                'button3':['замовіць тавар', 'make an order', 'сделать заказ']
                }


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton(buttons_language['button1'][language])
    button2 = types.KeyboardButton(buttons_language['button2'][language])
    button3 = types.KeyboardButton(buttons_language['button3'][language])
    markup.row(button1, button2)
    markup.row(button3)

    bot.send_message(message.chat.id, 'Вас вітае тэлеграм бот аўтарскай крамы адзення "ViA". У гэтым боце ў Вас ёсць магчымасць:', reply_markup=markup)


@bot.message_handler()
def info(message):
    if message.text in buttons_language['button1']:
        products(message)
    elif message.text in buttons_language['button2']:
        settings(message)
    elif message.text in buttons_language['button3']:
        make_order(message)
    elif message.text == '⬅️' or message.text == '➡️':
        products(message)
    elif message.text in config.TO_MAIN_MENU_BUTTON:
        start(message)
    elif message.text in config.CHANGE_LANGUAGE_TEXT:
        final_change_language(message)
    else:
        bot.send_message(message.chat.id, 'Oh i cant do that(')


def products(message):

    global i

    if message.text == '⬅️':

        if i!=0:
            i-=1
        else:
            i=2

    elif message.text == '➡️':

        if i == config.NUMBER_OF_AVAILABLE_PRODUCTS - 1:
            i=0
        else:
            i+=1    


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    button_left = types.KeyboardButton('⬅️')
    button_right = types.KeyboardButton('➡️')
    button_to_menu = types.KeyboardButton(config.TO_MAIN_MENU_BUTTON[language])

    markup.row(button_left, button_right)
    markup.row(button_to_menu)

    with open(config.PICTURES_OF_COSTUME[i][0], 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=config.DESCRIPTION[i][language], reply_markup=markup)


def make_order(message):
    webbrowser.open('https://t.me/flikersit')

def settings(message):

    markup = types.InlineKeyboardMarkup()

    button_change_language = types.InlineKeyboardButton(config.CHANGE_LANGUAGE_BUTTON[language], callback_data='language')
    button_contact_administrator = types.InlineKeyboardButton(config.CONTACT_ADMINISTRATOR_BUTTON[language], callback_data='admin')
    button_contact_designer = types.InlineKeyboardButton(config.CONTACT_DESIGNER_BUTTON[language], callback_data='design')
    button_contact_developer = types.InlineKeyboardButton(config.CONTACT_DEVELOPER_BUTTON[language], callback_data='dev')

    markup.row(button_change_language)
    markup.row(button_contact_administrator, button_contact_designer)
    markup.row(button_contact_developer)

    bot.send_message(message.chat.id, config.SETTING_TEXT[language], reply_markup=markup)


@bot.callback_query_handler(func=lambda callback=True)
def callback_message(callback, message):
    if callback.data == 'dev':
        webbrowser.open('https://t.me/flikersit')
    elif callback.data == 'language':
        changelanguage(message)


def changelanguage(message):
    markup = types.ReplyKeyboardMarkup()

    english = types.KeyboardButton('English')
    russian = types.KeyboardButton('Русский')
    belarussian = types.KeyboardButton('Беларусская')

    markup.row(english)
    markup.row(russian)
    markup.row(belarussian)

    bot.send_message(message.chat.id, config.CHANGE_LANGUAGE_TEXT[language])


def final_change_language(message):

    if message.txt == 'English':
        language=1
    elif message.txt == 'Русский':
        language = 2
    else:
        language = 0

    bot.send_message(message.chat.id, config.SUCCESS_CHANGE_LANGUAGE[language])
    
    start(message)
    


bot.polling(none_stop=True)
