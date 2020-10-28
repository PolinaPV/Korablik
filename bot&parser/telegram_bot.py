import json
import requests
from bs4 import BeautifulSoup
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import emoji

#   print(dir(emoji))
#   print(emoji.demojize('😉'))
#   print(emoji.emojize(':red_heart:'))
#   print('назад ' + emoji.emojize(':right_arrow_curving_left_selector:', variant="emoji_type"))

BASE_HOST = 'https://korablik-fond.ru/'
HELP_HOST = 'help/'
CHILD_HOST = 'our-children/'
CONTACT_HOST = 'contacts/'
REP_HOST = 'reporting/'
ABOUT_HOST = 'about/'
VACANS_HOST = 'vakansii/'
VOLONTER_HOST = 'join-us/'
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
BACK_MESS = 'Что ж, {}, посмотрим что еще я _могу сделать_ для вас'
RETURN_MESS = 'Могу помочь чем-нибудь ещё?' + emoji.emojize(':winking_face:')

#   Start menu Keyboard
button_need_help = KeyboardButton('Мне нужна помощь ' + emoji.emojize(':face_with_head-bandage:'))
button_can_help = KeyboardButton('Хочу помочь ' + emoji.emojize(':flexed_biceps:'))
button_need_info = KeyboardButton('Хочу знать чем занимается фонд ' + emoji.emojize(':face_with_monocle:'))
button_need_contact = KeyboardButton('Хочу получить контакты и реквизиты ' + emoji.emojize(':link:'))
button_volonter = KeyboardButton('Хочу стать волонтером' + emoji.emojize(':baby_angel_light_skin_tone:'))
button_need_work = KeyboardButton('Хочу работать у вас ' + emoji.emojize(':money_with_wings:'))
start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
start_markup.add(button_need_help, button_can_help, button_need_info)
start_markup.add(button_need_contact)
start_markup.add(button_volonter, button_need_work)
#   start_markup.row(button_need_work)
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
    # #   Кнопка "Мне нужна помощь"
    if message.text[0:3].lower() == 'мне' or message.text.lower() == 'помощь':
        telebot.types.ReplyKeyboardRemove
        mes = '\nПерейдите по ссылке на наш сайт и заполните форму обращения.'
        keyboard = InlineKeyboardMarkup()
        button_help_host = InlineKeyboardButton(text='Внешняя ссылка', url=BASE_HOST + HELP_HOST)
        keyboard.add(button_help_host)
        bot.send_message(message.chat.id, mes, reply_markup=keyboard)
        bot.send_message(message.chat.id, RETURN_MESS, reply_markup=back_markup)

    # #   Кнопка "Хочу помочь"
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
        bot.send_message(message.chat.id, RETURN_MESS, reply_markup=back_markup)

    # #   Кнопка "Чем занимается фонд"
    elif message.text[0:10].lower() == 'хочу знать' or message.text.lower() == 'фонд':
        telebot.types.ReplyKeyboardRemove
        bot.send_document(message.chat.id, PDF_FILE)
        mes = '\nБолее подробную информацию о фонде вы можете получить на соответствующей страничке сайта.'
        keyboad = InlineKeyboardMarkup()
        keyboad.add(InlineKeyboardButton('Внешняя ссылка', url=BASE_HOST + ABOUT_HOST))
        bot.send_message(message.chat.id, mes, reply_markup=keyboad)
        bot.send_message(message.chat.id, RETURN_MESS, reply_markup=back_markup)

    # #   Кнопка "Получить контакты и реквизиты"
    elif message.text[0:13].lower() == 'хочу получить' or message.text.lower() == 'получить':
        telebot.types.ReplyKeyboardRemove
        cont_req = get_contacts(parser(BASE_HOST + CONTACT_HOST).text)
        for dic in cont_req:
            mes_cont = '_Телефон: _' + str(dic['phone']) + '\n_Электронная почта: _' + \
                       str(dic['mail']) + '\n_Адрес: _' + str(dic['adres'])  # str(dic['links']) - соцсети
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Яндекс.Карты', url=str(dic['point'])))
            bot.send_message(message.chat.id, '*КОНТАКТЫ\n\n*' + mes_cont, reply_markup=keyboard, parse_mode='Markdown')

            mes_req = str(dic['regist']) + '\n' + str(dic['ogrn']) + '\n' + \
                      str(dic['inn']) + '\n' + str(dic['ur_adr']) + '\n' + str(dic['r_s']) + \
                      '\n' + str(dic['k_c']) + '\n' + str(dic['filial']) + '\n' + str(dic['bik']) + \
                      '\n' + str(dic['swift'])
            bot.send_message(message.chat.id, '*РЕКВИЗИТЫ\n\n*' + mes_req, parse_mode='Markdown')
        bot.send_message(message.chat.id, RETURN_MESS, reply_markup=back_markup)

    # #   Кнопка "Волонтер"
    elif message.text[0:10].lower() == 'хочу стать':
        telebot.types.ReplyKeyboardRemove
        mes = '*Это очень круто!* \nЧтобы стать нашим волонтером перейдите по ссылке и заполните форму.\n' + \
              get_volonter(parser(BASE_HOST + VOLONTER_HOST).text)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Внешняя ссылка', url=BASE_HOST + VOLONTER_HOST))
        bot.send_message(message.chat.id, mes, reply_markup=keyboard, parse_mode='Markdown')
        bot.send_message(message.chat.id, RETURN_MESS, reply_markup=back_markup)
    # #   Кнопка "Хочу работать"
    elif message.text[0:13].lower() == 'хочу работать':
        telebot.types.ReplyKeyboardRemove
        vacancy = get_vacancy(parser(BASE_HOST + VACANS_HOST).text)
        mes = 'На данный момент доступны следующие вакансии:\n\n'
        for div in vacancy:
            mes = mes + div + '\n'
            '''try:
                bot.send_message(message.chat.id, mes)
            except:
                print('Too long message')'''
        link_mes = '\nДля более подробной информации по вакансиям посетите *наш сайт*!'
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Внешняя ссылка', url=BASE_HOST + VACANS_HOST))
        bot.send_message(message.chat.id, mes + link_mes, reply_markup=keyboard, parse_mode='Markdown')
        help_mes = 'Если не нашли подходящей должности, вы можете просто прислать ваше резюме на почту hr@korablik-fond.ru' + \
            ' или присоединиться к волонтерской программе. Мы рады всем!'
        bot.send_message(message.chat.id, help_mes, parse_mode='Markdown')
        bot.send_message(message.chat.id, RETURN_MESS, reply_markup=back_markup)

    # # Кнопка "Назад"
    elif message.text[0:5].lower() == 'назад':
        bot.send_message(message.chat.id, BACK_MESS.format(message.chat.first_name),
                         reply_markup=start_markup, parse_mode='Markdown')

    else:
        try:
            bot.send_message(message.chat.id, 'Простите, я не знаю такой команды ' +
                             emoji.emojize(':pensive_face:') + '\n_Попробуйте еще раз!_', parse_mode='Markdown')
        except Exception as err:
            print('Something wrong! Exception: '.format(err))


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        bot.send_message(message.chat.id, 'Простите, я не знаю такой команды :(')
    except Exception as err:
        print('Something wrong! Exception: '.format(err))


def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req


def parser(url):
    html = get_html(url)
    if html.status_code == 200:
        return html
    else:
        print('Error status code')


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
        child.append(tmp)
    return child


def get_contacts(url):
    soup = BeautifulSoup(url, 'html5lib')
    ul = soup.find('div', class_='col-md-7').findAll('ul')
    #   ul[0] 1 - contacts
    #   ul[1] 2 - time
    #   ul[2] 3 - requizits
    #   ul[3] 4 - requizits too
    li_1 = ul[0].findAll('li')
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


def get_vacancy(url):
    soup = BeautifulSoup(url, 'html5lib')
    all_vac = soup.find('div', id='pgc-13480-2-0')
    vac = all_vac.findAll('div', class_='so-widget-sow-editor')
    vacancy = []
    for div in vac:
        tmp = div.find('h3', class_='widget-title')
        vacancy.append(tmp.get_text())
    return vacancy


def get_volonter(url):
    soup = BeautifulSoup(url, 'html5lib')
    descript = soup.find('p', class_='form-description').get_text()
    return descript

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


bot.polling(none_stop=True, interval=0)
