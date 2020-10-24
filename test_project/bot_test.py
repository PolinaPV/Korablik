import json
import requests
from bs4 import BeautifulSoup
import telebot
from telebot import types

BASE_HOST = 'https://korablik-fond.ru/'
HELP_HOST = 'help/'
CHILD_HOST = 'our-children/'
CONT_HOST = 'contacts/'
REP_HOST = 'reporting/'
ABOUT_HOST = 'about/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}

file = open('C:/Users/User/Documents/PycharmProjects/Korablik/token.txt', 'r')
TOKEN = file.read()
TEL_URL = 'https://api.telegram.org/bot'

bot = telebot.TeleBot(TOKEN)
START_MESS = 'Приветствую, {}! Я бот-помощник детского благотворительного фонда Кораблик. К вашим услугам!'

start_keyboards = types.InlineKeyboardMarkup(row_width=1)
need_help_keyboards = types.InlineKeyboardMarkup()
key_need_help = types.InlineKeyboardButton(text='Мне нужна помощь', callback_data='need_help')
key_can_help = types.InlineKeyboardButton(text='Хочу помочь', callback_data='can_help')
key_need_info = types.InlineKeyboardButton(text='Хочу знать, чем занимается фонд', callback_data='need_info')
key_pars = types.InlineKeyboardButton(text='Внешняя ссылка', url=BASE_HOST + HELP_HOST)
start_keyboards.add(key_need_help, key_can_help, key_need_info)
need_help_keyboards.add(key_pars)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, START_MESS.format(message.chat.first_name), reply_markup=start_keyboards)


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Message the developer', url='telegram.me/chernobrovka'
        )
    )
    bot.send_message(
        message.chat.id,
        '1) To receive a list of available currencies press /exchange.\n' +
        '2) Click on the currency you are interested in.\n' +
        '3) You will receive a message containing information regarding the source and the target currencies, ' +
        'buying rates and selling rates.\n' +
        '4) Click “Update” to receive the current information regarding the request. ' +
        'The bot will also show the difference between the previous and the current exchange rates.\n' +
        '5) The bot supports inline. Type @KorablikFondBot in any chat and the first letters of a currency.',
        reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'need_help':
        mes = 'Перейдите по ссылке на наш сайт и заполните форму обращения!'
        bot.send_message(call.message.chat.id, mes, reply_markup=need_help_keyboards)
    elif call.data == 'can_help':
        mes_1 = 'Это чудесно! Вот список детей, нуждающихся в помощи в данный момент:'
        bot.send_message(call.message.chat.id, mes_1)
        childs = parser(BASE_HOST + CHILD_HOST)
        #print(childs[0])
        #   print(x[1] for x in childs)
        for item in enumerate(childs):
            #   print(type(item))   #tuple
            #   print(type(childs))     #list
            tmp_ms = childs[item]
            #   tmp = json.load(i)
            #bot.send_message(call.message.chat.id, tmp_ms)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.send_message(message, 'Простите, я не знаю такой команды :(')
    except Exception as err:
        print('Something wrong! Exception: '.format(err))


def get_html(url):
    req = requests.get(url, headers=HEADERS)
    #   print(req)
    return req


def get_all_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    #   print(type(soup))
    #   print(soup)
    #   pg = soup.find('div', id='panel-689-1-0-2')  # Панель "Им нужна помощь"
    items = soup.find('div', id='panel-689-1-0-2').find_all('div', class_='child-card-content')
    child = []
    #   print(pg.text)
    for item in items:
        child.append(
            {
                'name': item.find('h4').get_text(strip=True),
                'info': [p.get_text(strip=True) for p in item.findAll('p')],  # it.find('p').get_text(),
                'link': item.find('div', class_='leyka-scale-button').find('a').get('href'),
                'money': [div.get_text() for div in item.findAll('div', class_='leyka-scale-label')],
                'img': item.find('div', class_='tpl-pictured-bg').get('style')
            })
    return child


def parser(url):
    html = get_html(url)
    if html.status_code == 200:
        child = []
        child.extend(get_all_content(html.text))
        return child
        #   print('\n'.join(map(str, parser(html))))
    else:
        print('Error status code')


bot.polling(none_stop=True, interval=0)
