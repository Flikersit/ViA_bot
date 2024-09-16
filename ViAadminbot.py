import telebot
import os
from telebot import types
import bcrypt

import config

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

bot = telebot.TeleBot(config.ADMIN_API_TOKEN)

i = 0

language = 2

user_status = {}
user_state = {}

def is_authenticated(user_id):
    return user_status.get(user_id, False)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    # Если пользователь еще не ввел пароль, запросим его
    if not is_authenticated(user_id):
        bot.send_message(user_id, "Введите пароль для доступа:")
    else:
        send_welcome_message(message)

# Функция для отправки приветственного сообщения после успешного ввода пароля
def send_welcome_message(message):
    markup = types.ReplyKeyboardMarkup

    button_contact_dev = types.KeyboardButton('Контакт разработчика')
    button_change_setup = types.KeyboardButton('Изменение ассортимента одежды')
    button_create_new_product = types.KeyboardButton('Добавить новый товар')

    markup.row(button_change_setup, button_contact_dev)
    markup.row(button_create_new_product)

    user_id = message.from_user.id
    bot.send_message(user_id, "Добро пожаловать! Теперь у вас есть доступ к функциям бота. Выберите, что вы хотите сделать", reply_markup=markup)

# Обработчик для сообщений с паролем
@bot.message_handler(func=lambda message: not is_authenticated(message.from_user.id), content_types=['text'])
def password_check(message):
    user_id = message.from_user.id

    # Проверяем введенный пароль
    if bcrypt.checkpw((message.text).encode('utf-8'), config.HASH):
        user_status[user_id] = True
        bot.send_message(user_id, "Пароль верный! Теперь у вас есть доступ.")
        send_welcome_message(message)
    else:
        bot.send_message(user_id, "Неверный пароль. Попробуйте снова:")

# Обработчик других команд и сообщений, доступный только после ввода пароля
@bot.message_handler(func=lambda message: is_authenticated(message.from_user.id), content_types=['text'])
def handle_authenticated_message(message):
    # Обработка команд и сообщений после успешного ввода пароля
    if user_state[message.from_user.id] == 'WAITING FOR PHOTO':
        bot.send_message(message.chat.id, 'Пожалуйста отправте сначала фото!')

    elif message.text.lower() == "команда":
        bot.send_message(message.from_user.id, "Вы можете использовать эту команду, так как ввели правильный пароль.")

    elif message.text == 'Изменение ассортимента одежды':
        change_clothes(message)

    elif message.text == 'Изменить доступность товара':
        change_available_clothes(message)

    elif message.text == 'Удалить продукт':
        del_product(message)

    else:
        bot.send_message(message.from_user.id, "Вы можете отправлять другие команды или сообщения.")


@bot.message_handler(func=lambda message: is_authenticated(message.from_user.id), content_types=['photo'])
def handle_authenticated_photo(message):
    user_id = message.from_user.id

    if user_state[user_id] == 'WAITING FOR PHOTO':

        for i in range(len(message.photo)):
            os.save('./')



def change_clothes(message):

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
    button_change_availabel = types.KeyboardButton('Изменить доступность товара')
    button_delite_product = types.KeyboardButton('Удалить продукт')

    markup.row(button_left, button_right)
    markup.row(button_to_menu)
    markup.row(button_change_availabel, button_delite_product)


    available = ''

    if config.AVAILABLE[i]:
        available += '✅' + '       ' + config.AVAILABLE_TEXT[language]
    else:
        available += '❌' + '       ' + config.NOT_AVAILABLE_TEXT[language]

    with open(config.PICTURES_OF_COSTUME[i][0], 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption=(config.DESCRIPTION[i][language] + '\n\n\n' + available), reply_markup=markup)


def change_available_clothes(message):

    config.AVAILABLE[i] = not config.AVAILABLE[i]

    bot.send_message(message.chat.id, "Статус наличия товара успешно изменен")

    start(message)


def del_product(message):

    config.NUMBER_OF_AVAILABLE_PRODUCTS -= 1
    os.remove(config.PICTURES_OF_COSTUME[i])
    config.DESCRIPTION.pop(i)
    config.PICTURES_OF_COSTUME.pop(i)

    bot.send_message(message.chat.id, 'Товар был успешно удален')
    start(message)



def upload_product_photo(message):

    user_id = message.from_user.id
    user_state[user_id] = 'WAITING FOR PHOTO'

    bot.send_message(message.chat.id, 'Отправте пожалуйста фото')




# Запуск бота
bot.polling(none_stop=True)

