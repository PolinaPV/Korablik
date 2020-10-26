import json
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import emoji

#   print(dir(emoji))
#   print(emoji.emojize('😔'))
#   print(emoji.emojize(':red_heart:'))
#   print('назад ' + emoji.emojize(':right_arrow_curving_left_selector:', variant="emoji_type"))

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

PDF_FILE = open('C:/Users/User/Documents/PycharmProjects/Korablik/Фонд Кораблик.pdf', 'rb')
TOKEN_FILE = open('C:/Users/User/Documents/PycharmProjects/Korablik/token.txt', 'r')
TOKEN = TOKEN_FILE.read()
#   TEL_URL = 'https://api.telegram.org/bot'

bot = telebot.TeleBot(TOKEN)
START_MESS = '*Приветствую, {}*' + emoji.emojize(':waving_hand_light_skin_tone:') + '\n\n' + \
             'Я _бот-помощник_ детского благотворительного фонда Кораблик. К вашим услугам!'
RE_MES = 'Что ж, {}, посмотрим что еще я _могу сделать_ для вас'

"""start_keyboards = InlineKeyboardMarkup(row_width=1)
key_need_help = InlineKeyboardButton(text='Мне нужна помощь', callback_data='need_help')
key_can_help = InlineKeyboardButton(text='Хочу помочь', callback_data='can_help')
key_need_info = InlineKeyboardButton(text='Хочу знать, чем занимается фонд', callback_data='need_info')
start_keyboards.add(key_need_help, key_can_help, key_need_info)"""

# Start menu RelayKeyboard
button_need_help = KeyboardButton('Мне нужна помощь ' + emoji.emojize(':face_with_head-bandage:'))
button_can_help = KeyboardButton('Хочу помочь ' + emoji.emojize(':flexed_biceps:'))
button_need_info = KeyboardButton('Хочу знать чем занимается фонд ' + emoji.emojize(':face_with_monocle:'))
button_need_contact = KeyboardButton('Хочу получить контакты и реквизиты ' + emoji.emojize(':link:'))
start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
start_markup.add(button_need_help, button_can_help, button_need_info)
start_markup.row(button_need_contact)
#   Back Button
button_back = KeyboardButton('Назад️ ' + emoji.emojize(':right_arrow_curving_left_selector:'))
back_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, )
back_markup.add(button_back)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, START_MESS.format(message.chat.first_name),
                     reply_markup=start_markup, parse_mode='Markdown')


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton(
            'Message the developer', url='telegram.me/chernobrovka'
        )
    )
    bot.send_message(
        message.chat.id,
        'You can send message to developer!',
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['text'])
def need_help_command(message):
    #   bot.send_message(message.chat.id, message.text[0:])
    if message.text[0:3].lower() == 'мне' or message.text.lower() == 'помощь':
        telebot.types.ReplyKeyboardRemove
        mes = '\nПерейдите по ссылке на наш сайт и заполните форму обращения.'
        keyboard = InlineKeyboardMarkup()
        button_help_host = InlineKeyboardButton(text='Внешняя ссылка', url=BASE_HOST + HELP_HOST)
        keyboard.add(button_help_host)
        bot.send_message(message.chat.id, mes, reply_markup=keyboard)
        bot.send_message(message.chat.id, 'Могу помочь чем-нибудь ещё?', reply_markup=back_markup)

    elif message.text[0:11].lower() == 'хочу помочь' or message.text.lower() == 'помочь':
        telebot.types.ReplyKeyboardRemove
        mes_1 = 'Это чудесно! Вот список детей, нуждающихся в помощи в данный момент:'
        bot.send_message(message.chat.id, mes_1)
        childs = get_all_content(parser(BASE_HOST + CHILD_HOST).text)
        for dic in childs:
            mes = '*' + str(dic['name']) + '*\n\n' + str(dic['age']) + '\n' + str(dic['city']) + \
                  '\n' + str(dic['diagnoz']) + '\n' + '\n_' + str(dic['money'] + '_')
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Помочь прямо сейчас!', url=str(dic['link'])))
            bot.send_photo(message.chat.id, str(dic['img']))
            bot.send_message(message.chat.id, mes +
                             '\n\nДля более подробной информации перейдите по _ссылке_ на страничку ребенка.',
                             reply_markup=keyboard, parse_mode='Markdown')
        bot.send_message(message.chat.id, 'Могу помочь чем-нибудь ещё?', reply_markup=back_markup)

    elif message.text[0:10].lower() == 'хочу знать' or message.text.lower() == 'фонд':
        telebot.types.ReplyKeyboardRemove
        bot.send_document(message.chat.id, PDF_FILE)
        mes = '\nБолее подробную информацию о фонде вы можете получить на соответствующей страничке сайта.'
        keyboad = InlineKeyboardMarkup()
        keyboad.add(InlineKeyboardButton('Внешняя ссылка', url=BASE_HOST + ABOUT_HOST))
        bot.send_message(message.chat.id, mes, reply_markup=keyboad)
        bot.send_message(message.chat.id, 'Могу помочь чем-нибудь ещё?', reply_markup=back_markup)

    elif message.text[0:13].lower() == 'хочу получить' or message.text.lower() == 'получить':
        telebot.types.ReplyKeyboardRemove
        cont_req = get_contacts(parser(BASE_HOST + CONT_HOST).text)
        for dic in cont_req:
            #   print(type(cont_req))
            mes_cont = '_Телефон: _' + str(dic['phone']) + '\n_Электронная почта: _' + \
                  str(dic['mail']) + '\n_Адрес: _' + str(dic['adres'])  # str(dic['links']) - соцсети
            keyboard = InlineKeyboardMarkup()
            #   print(str(dic['point']))
            keyboard.add(InlineKeyboardButton('Яндекс.Карты', url=str(dic['point'])))
            bot.send_message(message.chat.id, '*КОНТАКТЫ\n\n*' + mes_cont, reply_markup=keyboard, parse_mode='Markdown')

            mes_req = str(dic['regist']) + '\n' + str(dic['ogrn']) + '\n' + \
                str(dic['inn']) + '\n' + str(dic['ur_adr']) + '\n' + str(dic['r_s']) + \
                '\n' + str(dic['k_c']) + '\n' + str(dic['filial']) + '\n' + str(dic['bik']) + \
                '\n' + str(dic['swift'])
            #   keyboard_2 = InlineKeyboardMarkup()
            #   keyboard_2.add(InlineKeyboardButton(''))
            bot.send_message(message.chat.id, '*РЕКВИЗИТЫ\n\n*' + mes_req, parse_mode='Markdown')

        bot.send_message(message.chat.id, 'Могу помочь чем-нибудь ещё?', reply_markup=back_markup)

    elif message.text[0:5].lower() == 'назад':
        bot.send_message(message.chat.id, RE_MES.format(message.chat.first_name),
                         reply_markup=start_markup, parse_mode='Markdown')

    else:
        try:
            bot.send_message(message.chat.id, 'Простите, я не знаю такой команды ' +
                             emoji.emojize(':pensive_face:') + '\n_Попробуйте еще раз!_', parse_mode='Markdown')
        except Exception as err:
            print('Something wrong! Exception: '.format(err))


"""@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == 'need_help':
        mes = '\nПерейдите по ссылке на наш сайт и заполните форму обращения.'
        bot.send_message(call.message.chat.id, mes, reply_markup=need_help_keyboards)
    elif call.data == 'can_help':
        mes_1 = '\nЭто чудесно! Вот список детей, нуждающихся в помощи в данный момент:'
        bot.send_message(call.message.chat.id, mes_1)
        childs = parser(BASE_HOST + CHILD_HOST)
        for dic in childs:
            mes = str(dic['name']) + '\n\n' + str(dic['age']) + '\n' + str(dic['city']) + \
                  '\n' + str(dic['diagnoz']) + '\n' + '\n' + str(dic['money'])

            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(
                'Помочь прямо сейчас!', url=str(dic['link'])
            ))
            bot.send_photo(call.message.chat.id, str(dic['img']))
            bot.send_message(call.message.chat.id, mes +
                             '\n\nДля более подробной информации перейдите по ссылке на страничку ребенка.',
                             reply_markup=keyboard)
    elif call.data == 'need_info':
        mes = '\nВсю информацию о  фонде вы можете получить на соответствующей страничке сайта.'
        keyboad = InlineKeyboardMarkup()
        keyboad.add(InlineKeyboardButton('Внешняя ссылка', url=BASE_HOST + ABOUT_HOST))
        bot.send_message(call.message.chat.id, mes, reply_markup=keyboad)"""


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.send_message(message.chat.id, 'Простите, я не знаю такой команды :(')
    except Exception as err:
        print('Something wrong! Exception: '.format(err))


def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req


def get_all_content(html):
    soup = BeautifulSoup(html, 'html5lib')
    items = soup.find('div', id='panel-689-1-0-2').find_all('div', class_='child-card-content')
    child = []
    for item in items:
        infos = item.findAll('p')
        tmp = dict({
            'name': item.find('h4').get_text(strip=True),
            'age': infos[0].get_text(),
            'city': infos[1].get_text(),
            'diagnoz': infos[2].get_text(),
            'link': item.find('div', class_='leyka-scale-button').find('a').get('href'),
            'money': item.find('div', class_='leyka-scale-label').get_text().strip(),
            'img': item.find('div', class_='tpl-pictured-bg').get('style')
        })
        tmp = get_clear_link(tmp)
        child.append(tmp)  # json.dumps(tmp, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': ')))
    return child


def get_contacts(url):
    soup = BeautifulSoup(url, 'html5lib')
    ul = soup.find('div', class_='col-md-7').findAll('ul')
    #   ul[0] 1 - contacts
    #   ul[1] 2 - time
    #   ul[2] 3 - requizits
    #   ul[3] 4 - requizits too
    li_1 = ul[0].findAll('li')
    #   li_2 = cont[1].findAll('li')
    li_3 = ul[2].findAll('li')
    li_4 = ul[3].findAll('li')
    cont_req = []
    for dic in li_1:
        contact = dict({
            'phone': li_1[0].find('span').get_text() + li_1[0].find('a').get('href'),
            'mail': li_1[1].find('span').get_text() + li_1[1].find('a').get('href'),
            'adres': li_1[2].find('span').get_text() + li_1[2].find('a').get_text(),
            'point': li_1[2].find('span').get_text() + li_1[2].find('a').get('href'),
            'links': [div.get('href') for div in li_1[3].findAll('a')]})
        # })
        """time = dict({
            'mon': li_2[0].get_text(),
            'tue': li_2[1].get_text(),
            'wed': li_2[2].get_text(),
            'thu': li_2[3].get_text(),
            'fri': li_2[4].get_text(),
            'sut': li_2[5].get_text(),
            'sun': li_2[6].get_text()
        })"""
        # requiz = dict({
    for dic in li_3:
        contact.update({
            'regist': li_3[0].get_text(strip=True),
            'ogrn': li_3[1].get_text(),
            'inn': li_3[2].get_text(),
            'ur_adr': li_3[3].get_text(strip=True)})
    for dic in li_4:
        contact.update({
            'r_s': li_4[0].get_text(),
            'k_c': li_4[1].get_text(),
            'filial': li_4[2].get_text(strip=True),
            'bik': li_4[3].get_text(),
            'swift': li_4[4].get_text()
        })
    contact = get_clear_contacts(contact)
    cont_req.append(contact)
    return cont_req
    """soup = BeautifulSoup(url, 'html5lib')
    cont = soup.find('div', class_='col-md-7').findAll('ul')
    #   ul[0] 1 - contacts
    #   ul[1] 2 - time
    #   ul[2] 3 - requizits
    #   ul[3] 4 - requizits too
    li_1 = cont[0].findAll('li')
    cont_req =[]
    contact = dict({
        'phone': li_1[0].find('span').get_text() + li_1[0].find('a').get('href'),
        'mail': li_1[1].find('span').get_text() + li_1[1].find('a').get('href'),
        'adres': li_1[2].find('span').get_text() + li_1[2].find('a').get_text(),
        'point': li_1[2].find('span').get_text() + li_1[2].find('a').get('href'),
        'links': [div.get('href') for div in li_1[3].findAll('a')]
    })
    li_2 = cont[1].findAll('li')
    time = dict({
        'mon': li_2[0].get_text(),
        'tue': li_2[1].get_text(),
        'wed': li_2[2].get_text(),
        'thu': li_2[3].get_text(),
        'fri': li_2[4].get_text(),
        'sut': li_2[5].get_text(),
        'sun': li_2[6].get_text()
    })
    li_3 = cont[2].findAll('li')
    li_4 = cont[3].findAll('li')
    requiz = dict({
        'regist': li_3[0].get_text(strip=True),
        'ogrn': li_3[1].get_text(),
        'inn': li_3[2].get_text(),
        'ur_adres': li_3[3].get_text(strip=True),
        'r_s': li_4[0].get_text(),
        'k_c': li_4[1].get_text(),
        'filial': li_4[2].get_text(strip=True),
        'bik': li_4[3].get_text(),
        'swift': li_4[4].get_text()
    })
    contact = get_clear_contacts(contact)
    return contact"""  # , requiz


def get_clear_link(dictionary):
    for key, value in dictionary.items():
        if key.find('img') != -1:
            i_beg = value.find('url(')
            i_end_jpg = value.rfind('jpg')
            i_end_jpeg = value.rfind('jpeg')
            i_end_png = value.rfind('png')
            if i_beg != -1 & (i_end_jpg != -1 | i_end_jpeg != -1 | i_end_png != -1):
                if i_end_jpg != -1:
                    dictionary.update({'img': value[i_beg + 4: i_end_jpg + 3]})
                elif i_end_png != -1:
                    dictionary.update({'img': value[i_beg + 4: i_end_png + 3]})
                else:
                    dictionary.update({'img': value[i_beg + 4: i_end_jpeg + 4]})
    return dictionary


def get_clear_contacts(dictionary):
    for key, value in dictionary.items():
        if key.find('mail') != -1:
            i_beg = value.find('info')
            i_end = value.rfind('.ru')
            if i_beg != -1 & i_end != -1:
                dictionary.update({'mail': value[i_beg: i_end + 3]})
        elif key.find('phone') != -1:
            i_beg = value.find('+')
            i_end = value.rfind('41')
            if i_beg != -1 & i_end != -1:
                dictionary.update({'phone': value[i_beg: i_end + 2]})
        elif key.find('adres') != -1:
            i_beg = value.find('11')
            i_end = value.rfind('34')
            if i_beg != -1 & i_end != -1:
                dictionary.update({'adres': value[i_beg: i_end + 2]})
        elif key.find('point') != -1:
            i_beg = value.find('https')
            i_end = value.rfind('X6q')
            if i_beg != -1 & i_end != -1:
                dictionary.update({'point': value[i_beg: i_end + 3]})
    return dictionary


def parser(url):
    html = get_html(url)
    if html.status_code == 200:
        #child = []
        #child.extend(get_all_content(html.text))
        return html
    else:
        print('Error status code')


bot.polling(none_stop=True, interval=0)
