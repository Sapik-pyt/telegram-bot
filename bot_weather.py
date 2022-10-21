import telebot
import os
from telebot import types
from weather import get_weather
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('token')
open_weather_token = os.getenv('wea_token')
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        text=f'Hello, {message.from_user.username}'
    )

@bot.message_handler(commands=['info'])
def get_user_info(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(
        text='Серьезно?',
        callback_data='yes'
    )
    item_no = types.InlineKeyboardButton(
        text='Ну вер',
        callback_data='no'
    )
    markup_inline.add(item_yes, item_no)
    bot.send_message(
        message.chat.id,
        text='Я все знаю о вас',
        reply_markup=markup_inline
    )

@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        type_yes = types.KeyboardButton('Мой ID')
        type_no = types.KeyboardButton('Мое имя')
        markup_reply.add(type_no, type_yes)
        bot.send_message(
            call.message.chat.id,
            'Нажмите на одну из кнопок',
            reply_markup=markup_reply
        )
    elif call.data == 'no':
        pass

@bot.message_handler(content_types=['text'])
def get_user_id(message):
    if message.text == 'Мой ID':
        bot.send_message(
            message.chat.id,
            text=f'Ваш ID: {message.from_user.id}'
        )
    elif message.text == 'Мое имя':
        bot.send_message(
            message.chat.id,
            text=f'Ваше имя: {message.from_user.first_name}'
        ) 

@bot.message_handler(content_types=['text'], commands=['talk'])   
def get_text(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, 'Hello')
    elif message.text.lower() == 'как дела ?':
        bot.send_message(message.chat.id, 'Все хорошо, а у тебя?☺️')

@bot.message_handler(commands=['weather'], content_types=['text'])
def weather_now(message):
    markup_inline = types.ReplyKeyboardMarkup()
    markup_inline.add(
        types.KeyboardButton('Да'),
        types.KeyboardButton('Нет')
    )
    mem = bot.send_message(
        message.chat.id,
        'Хотите узнать погоду?',
        reply_markup=markup_inline
    )
    bot.register_next_step_handler(mem, answer_two)

def answer_two(message):
    if message.text == 'Да':
        msg = bot.send_message(
            message.chat.id,
            'Введите ваш город',
        )
        bot.register_next_step_handler(msg, get_weat)

def get_weat(message):
    bot.send_message(
        message.chat.id,
        f'{get_weather(city=message.text,open_weather_token=open_weather_token)}'
    )

bot.polling(none_stop=True, interval=0)
