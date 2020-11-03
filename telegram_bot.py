import config
import logging
import urllib.request
import pars
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import emoji
from sqliter import SQLiter

#   print(emoji.demojize('😉'))
#   print(emoji.emojize(':red_heart:'))
#   print('назад ' + emoji.emojize(':right_arrow_curving_left_selector:', variant="emoji_type"))

logging.basicConfig(level=logging.INFO)

BASE_HOST = 'https://korablik-fond.ru/'
HELP_HOST = 'help/'
CHILD_HOST = 'our-children/'
CONTACT_HOST = 'contacts/'
#   REP_HOST = 'reporting/'
ABOUT_HOST = 'about/'
VACANS_HOST = 'vakansii/'
VOLONTER_HOST = 'join-us/'

PDF_FILE = open('Фонд Кораблик.pdf', 'rb')

bot = telebot.TeleBot(config.TOKEN)
#   print(dir(bot))
START_MESS = '*Приветствую, {}* ' + emoji.emojize(':waving_hand_light_skin_tone:') + '\n\n' + \
             'Я _бот-помощник_ детского благотворительного фонда Кораблик. К вашим услугам!'
FEEDBACK_MESS = 'Могу помочь чем-нибудь ещё? ' + emoji.emojize(':winking_face:')
RETURN_MESS = 'Что ж, {}, посмотрим что еще я могу сделать для вас'

#   Start menu Keyboard
button_need_help = KeyboardButton('Мне нужна помощь')  # + emoji.emojize(':face_with_head-bandage:'))
button_can_help = KeyboardButton('Хочу помочь')  # + emoji.emojize(':flexed_biceps:'))
button_need_info = KeyboardButton('Хочу знать чем занимается фонд')  # + emoji.emojize(':face_with_monocle:'))
button_need_contact = KeyboardButton('Хочу получить контакты и реквизиты')  # + emoji.emojize(':link:'))
button_volonter = KeyboardButton('Хочу стать волонтером')  # + emoji.emojize(':baby_angel_light_skin_tone:'))
button_need_work = KeyboardButton('Хочу работать у вас')  # + emoji.emojize(':money_with_wings:'))
start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
start_markup.add(button_need_help, button_can_help, button_need_info)
start_markup.add(button_need_contact)
start_markup.add(button_volonter, button_need_work)
#   Back button Keyboard
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
    keyboard.add(InlineKeyboardButton('Message the developer', url='telegram.me/chernobrovka'))
    bot.send_message(message.chat.id, 'You can send message to developer!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def need_help_command(message):
    #   bot.send_message(message.chat.id, message.text[0:])
    # #   Кнопка "Мне нужна помощь"
    if message.text[0:3].lower() == 'мне' or message.text.lower() == 'помощь':
        try:
            infos = pars.get_memo(pars.get_parser(BASE_HOST + HELP_HOST).text)
            mes = '\nПерейдите по ссылке на наш сайт и заполните форму обращения.\n\n' + \
                  str(infos['lead']) + str(infos['spisok'])
            keyboard = InlineKeyboardMarkup()
            button_help_host = InlineKeyboardButton(text='Внешняя ссылка', url=BASE_HOST + HELP_HOST)
            keyboard.add(button_help_host)
            bot.send_message(message.chat.id, mes, reply_markup=keyboard)
            bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)
        except:
            print("error get_memo")

    # #   Кнопка "Хочу помочь"
    elif message.text[0:11].lower() == 'хочу помочь' or message.text.lower() == 'помочь':
        mes_1 = 'Это чудесно! Вот список детей, нуждающихся в помощи в данный момент:'
        bot.send_message(message.chat.id, mes_1)
        childs = pars.get_all_content(pars.get_parser(BASE_HOST + CHILD_HOST).text)
        for dic in childs:
            mes = '*' + str(dic['name']) + '*\n\n' + str(dic['age']) + '\n' + str(dic['city']) + \
                  '\n' + str(dic['diagnoz']) + '\n' + '\n_' + str(dic['money'] + '_')
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Помочь прямо сейчас!', url=str(dic['link'])))
            bot.send_photo(message.chat.id, str(dic['img']))
            bot.send_message(message.chat.id, mes +
                             '\n\nДля более подробной информации перейдите по _ссылке_ на страничку ребенка.',
                             reply_markup=keyboard, parse_mode='Markdown')
        bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)

    # #   Кнопка "Чем занимается фонд"
    elif message.text[0:10].lower() == 'хочу знать' or message.text.lower() == 'фонд':
        bot.send_document(message.chat.id, PDF_FILE)
        mes = '\nБолее подробную информацию о фонде вы можете получить на соответствующей страничке сайта.'
        keyboad = InlineKeyboardMarkup()
        keyboad.add(InlineKeyboardButton('Внешняя ссылка', url=BASE_HOST + ABOUT_HOST))
        bot.send_message(message.chat.id, mes, reply_markup=keyboad)

        bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)

    # #   Кнопка "Получить контакты и реквизиты"
    elif message.text[0:13].lower() == 'хочу получить' or message.text.lower() == 'получить':
        cont_req = pars.get_contacts(pars.get_parser(BASE_HOST + CONTACT_HOST).text)
        for dic in cont_req:
            mes_cont = '_Телефон: _' + str(dic['phone']) + '\n_Электронная почта: _' + \
                       str(dic['mail']) + '\n_Адрес: _' + str(dic['adres'])  # str(dic['links']) - соцсети
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Яндекс.Карты', url=str(dic['point'])))
            bot.send_message(message.chat.id, '*КОНТАКТЫ\n\n*' + mes_cont, reply_markup=keyboard, parse_mode='Markdown')
            link_mess = 'Ссылки на соцсети:'
            link_keyboard = InlineKeyboardMarkup(row_width=2)
            vk_link = InlineKeyboardButton('ВКонтакте', url=dic['links'][0])
            fb_link = InlineKeyboardButton('Facebook', url=dic['links'][1])
            ins_link = InlineKeyboardButton('Instagram', url=dic['links'][2])
            ok_link = InlineKeyboardButton('Одноклассники', url=dic['links'][3])
            link_keyboard.add(vk_link, fb_link, ins_link, ok_link)
            bot.send_message(message.chat.id, link_mess, reply_markup=link_keyboard)

            mes_req = str(dic['regist']) + '\n' + str(dic['ogrn']) + '\n' + \
                      str(dic['inn']) + '\n' + str(dic['ur_adr']) + '\n' + str(dic['r_s']) + \
                      '\n' + str(dic['k_c']) + '\n' + str(dic['filial']) + '\n' + str(dic['bik']) + \
                      '\n' + str(dic['swift'])
            bot.send_message(message.chat.id, '*РЕКВИЗИТЫ\n\n*' + mes_req, parse_mode='Markdown')
        bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)

    # #   Кнопка "Волонтер"
    elif message.text[0:10].lower() == 'хочу стать':
        mes = '*Это очень круто!* \nЧтобы стать нашим волонтером перейдите по ссылке и заполните форму.\n' + \
              pars.get_volonter(pars.get_parser(BASE_HOST + VOLONTER_HOST).text)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Внешняя ссылка', url=BASE_HOST + VOLONTER_HOST))
        bot.send_message(message.chat.id, mes, reply_markup=keyboard, parse_mode='Markdown')
        bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)

    # #   Кнопка "Хочу работать"
    elif message.text[0:13].lower() == 'хочу работать':
        vacancy = pars.get_vacancy(pars.get_parser(BASE_HOST + VACANS_HOST).text)
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
        bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)

    # # Кнопка "Назад"
    elif message.text[0:5].lower() == 'назад':
        bot.send_message(message.chat.id, RETURN_MESS.format(message.chat.first_name),
                         reply_markup=start_markup, parse_mode='Markdown')

    else:
        try:
            bot.send_message(message.chat.id, 'Простите, я не знаю такой команды ' +
                             emoji.emojize(':pensive_face:') + '\n*Попробуйте еще раз!*', parse_mode='Markdown')
        except Exception as err:
            print('Something wrong! Exception: '.format(err))


@bot.message_handler(content_types=['document'])
def handle_doc(message):
    doc_id = message.document.file_id
    file_info = bot.get_file(doc_id)
    #   file.file_path = 'C:/Users/User/Documents/PycharmProjects/Korablik/'
    print(file_info)
    #   print(file.file_path)
    try:
        urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{config.TOKEN}/{file_info.file_path}',
                                   file_info.file_path)
        bot.send_message(message.chat.id, 'Спасибо, ваше резюме принято!')
    except:
        print('Error get file')


@bot.message_handler(func=lambda message: True)
def error_command(message):
    try:
        bot.send_message(message.chat.id, 'Простите, я не знаю такой команды :(')
    except Exception as err:
        print('Something wrong! Exception: '.format(err))


def main():
    bot.polling(none_stop=True, interval=0)


if __name__ == '__main__':
    main()
