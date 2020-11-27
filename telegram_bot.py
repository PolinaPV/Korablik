import config
from loguru import logger
import pars
import asyncio
from aiogram import Dispatcher, executor, Bot
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.exceptions import FileIsTooBig
import urllib.request
import emoji
"""  
#   telebot не ассинхронная либа, не вариант для рассылки  
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
import logging  # Change to loguru
"""

#   print(emoji.demojize('👍🏻'))     # Декодирование эмоджи
#   logging.basicConfig(filename='korablik.log', format='\n%(name)s - %(levelname)s - %(message)s', level=logging.INFO)


logger.add('debug_korablik.log', format='\t{time}  {level}  {message}\n\n',
           level='ERROR', rotation='1 week', compression='zip')  # , serialize=True)     #   Для json формата

bot = Bot(token=config.TOKEN)
dis = Dispatcher(bot)
db = config.DB  # База данных юзеров
pdf_file = config.PDF_FILE  # Презентация фонда
loop = asyncio.get_event_loop()

BASE_HOST = 'https://korablik-fond.ru/'
HELP_HOST = 'help/'
CHILD_HOST = 'our-children/'
CONTACT_HOST = 'contacts/'
ABOUT_HOST = 'about/'
VACANS_HOST = 'vakansii/'
VOLONTER_HOST = 'join-us/'

START_MESS = '*Приветствую, {}* ' + emoji.emojize(':waving_hand_light_skin_tone:') + '\n\n' + \
             'Я _бот-помощник_ детского благотворительного фонда Кораблик. К вашим услугам!'
FEEDBACK_MESS = 'Могу помочь чем-нибудь ещё? ' + emoji.emojize(':winking_face:')
RETURN_MESS = 'Что ж, {}, посмотрим, что еще я могу сделать для вас.'
LINK_TRACK = 'utm_source=tg_bot&utm_medium=content&utm_campaign=general&utm_content={}'

#   Start menu Keyboard
button_need_help = KeyboardButton('Мне нужна помощь')  # + emoji.emojize(':face_with_head-bandage:'))
button_can_help = KeyboardButton('Хочу помочь')  # + emoji.emojize(':flexed_biceps:'))
button_need_info = KeyboardButton('Хочу знать чем занимается фонд')  # + emoji.emojize(':face_with_monocle:'))
button_need_contact = KeyboardButton('Хочу получить контакты и реквизиты')  # + emoji.emojize(':link:'))
button_volonter = KeyboardButton('Хочу стать волонтером')  # + emoji.emojize(':baby_angel_light_skin_tone:'))
button_need_work = KeyboardButton('Хочу работать у вас')  # + emoji.emojize(':money_with_wings:'))
subscription_button = InlineKeyboardButton('Управление подпиской')
start_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
start_markup.add(button_need_help, button_can_help, button_need_info)
start_markup.add(button_need_contact)
start_markup.add(button_volonter, button_need_work)
start_markup.add(subscription_button)
#   Back button Keyboard
button_back = KeyboardButton('Назад️ ' + emoji.emojize(':right_arrow_curving_left_selector:'))
back_markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, )
back_markup.add(button_back)
#   Subscription/unsubscription Keyboard
yes_subscribe = InlineKeyboardButton('Да ' + emoji.emojize(':thumbs_up_light_skin_tone:'), callback_data='yes')
no_subscribe = InlineKeyboardButton('Нет ' + emoji.emojize(':thumbs_down_light_skin_tone:'), callback_data='no')
yes_unsubscribe = InlineKeyboardButton('Да ' + emoji.emojize(':thumbs_down_light_skin_tone:'), callback_data='no')
no_unsubscribe = InlineKeyboardButton('Нет ' + emoji.emojize(':thumbs_up_light_skin_tone:'), callback_data='yes')
subscription_keyboard = InlineKeyboardMarkup()
unsubscription_keyboard = InlineKeyboardMarkup()
subscription_keyboard.add(yes_subscribe, no_subscribe)
unsubscription_keyboard.add(yes_unsubscribe, no_unsubscribe)


@dis.message_handler(commands=['start'])
async def start_command(message):
    if not db.users_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        print('user add')
    else:
        pass
    await bot.send_message(message.chat.id, START_MESS.format(message.chat.first_name),
                           reply_markup=start_markup, parse_mode='Markdown')


@dis.message_handler(commands=['help'])
async def help_command(message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton('Message the developer', url='telegram.me/chernobrovka'))
    await bot.send_message(message.chat.id, 'You can send message to developer!', reply_markup=keyboard)


@dis.message_handler(content_types=['text'])
async def need_help_command(message):
    """ Обработчик всех кнопок стартовой клавиатуры """
    #   bot.send_message(message.chat.id, message.text[0:])
    # #   Кнопка "Мне нужна помощь"
    if message.text[0:3].lower() == 'мне' or message.text.lower() == 'помощь':
        try:
            infos = pars.get_memo(pars.get_parser(BASE_HOST + HELP_HOST).text)
            mes = '\nПерейдите по ссылке на наш сайт и заполните форму обращения.\n\n' + \
                  str(infos['lead']) + str(infos['spisok'])
            keyboard = InlineKeyboardMarkup()
            button_help_host = InlineKeyboardButton(text='Внешняя ссылка',
                                                    url=BASE_HOST + '?' + HELP_HOST + LINK_TRACK.format(
                                                        message.from_user.id))
            keyboard.add(button_help_host)
            await bot.send_message(message.chat.id, mes, reply_markup=keyboard)
            await bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)
        except Exception as error:
            print("error get_memo: {}".format(error))

    # #   Кнопка "Хочу помочь"
    elif message.text[0:11].lower() == 'хочу помочь' or message.text.lower() == 'помочь':
        mes_1 = 'Это чудесно! Вот список детей, нуждающихся в помощи в данный момент:'
        await bot.send_message(message.chat.id, mes_1)
        # t_start = perf_counter()
        childs = pars.get_all_content(pars.get_parser(BASE_HOST + CHILD_HOST).text)
        # t_stop = perf_counter()
        # print("Elapsed time:", t_start, t_stop)
        for dic in childs:
            mes = '*' + str(dic['name']) + '*\n\n' + str(dic['age']) + '\n' + str(dic['city']) + \
                  '\n' + str(dic['diagnoz']) + '\n' + '\n_' + str(dic['money'] + '_')
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Помочь прямо сейчас!',
                                              url=str(dic['link']) + '&' + LINK_TRACK.format(
                                                  message.from_user.id)))
            await bot.send_photo(message.chat.id, str(dic['img']))
            await bot.send_message(message.chat.id, mes +
                                   '\n\nДля более подробной информации перейдите по _ссылке_ на страничку ребенка.',
                                   reply_markup=keyboard, parse_mode='Markdown')
        await bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)

    # #   Кнопка "Чем занимается фонд"
    elif message.text[0:10].lower() == 'хочу знать' or message.text.lower() == 'фонд':
        await bot.send_document(message.chat.id, pdf_file)
        mes = '\nВы можете ознакомится с наей презентацией! \n' \
              'Более подробную информацию о фонде вы можете получить на соответствующей страничке сайта.'
        keyboad = InlineKeyboardMarkup()
        keyboad.add(InlineKeyboardButton('Внешняя ссылка', url=BASE_HOST + ABOUT_HOST))
        await bot.send_message(message.chat.id, mes, reply_markup=keyboad)
        await bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)

    # #   Кнопка "Получить контакты и реквизиты"
    elif message.text[0:13].lower() == 'хочу получить' or message.text.lower() == 'получить':
        cont_req = pars.get_contacts(pars.get_parser(BASE_HOST + CONTACT_HOST).text)
        for dic in cont_req:
            mes_cont = '\n_Телефон: _' + str(dic['phone']) + '\n_Электронная почта: _' + \
                       str(dic['mail']) + '\n_Адрес: _' + str(dic['adres'])  # str(dic['links']) - соцсети
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton('Яндекс.Карты',
                                              url=str(dic['point']) + '&' + LINK_TRACK.format(
                                                  message.from_user.id)))
            await bot.send_message(message.chat.id, '*КОНТАКТЫ\n*' + mes_cont, reply_markup=keyboard,
                                   parse_mode='Markdown')
            link_mess = 'Ссылки на соцсети:'
            link_keyboard = InlineKeyboardMarkup(row_width=2)
            vk_link = InlineKeyboardButton('ВКонтакте', url=dic['links'][0])
            fb_link = InlineKeyboardButton('Facebook', url=dic['links'][1])
            ins_link = InlineKeyboardButton('Instagram', url=dic['links'][2])
            ok_link = InlineKeyboardButton('Одноклассники', url=dic['links'][3])
            link_keyboard.add(vk_link, fb_link, ins_link, ok_link)
            await bot.send_message(message.chat.id, link_mess, reply_markup=link_keyboard)
            mes_req = str(dic['regist']) + '\n' + str(dic['ogrn']) + '\n' + str(dic['inn']) + '\n' + \
                      str(dic['ur_adr']) + '\n' + str(dic['r_s']) + '\n' + str(dic['k_c']) + '\n' + \
                      str(dic['filial']) + '\n' + str(dic['bik']) + '\n' + str(dic['swift'])
            await bot.send_message(message.chat.id, '*РЕКВИЗИТЫ\n\n*' + mes_req, parse_mode='Markdown')
        await bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)

    # #   Кнопка "Волонтер"
    elif message.text[0:10].lower() == 'хочу стать':
        mes = '*Это очень круто!* \nЧтобы стать нашим волонтером перейдите по ссылке и заполните форму.\n' + \
              pars.get_volonter(pars.get_parser(BASE_HOST + VOLONTER_HOST).text)
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton('Внешняя ссылка',
                                          url=BASE_HOST + VOLONTER_HOST + '?' + LINK_TRACK.format(
                                              message.from_user.id)))
        await bot.send_message(message.chat.id, mes, reply_markup=keyboard, parse_mode='Markdown')
        await bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)

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
        keyboard.add(InlineKeyboardButton('Внешняя ссылка',
                                          url=BASE_HOST + VACANS_HOST + '?' + LINK_TRACK.format(
                                              message.from_user.id)))
        await bot.send_message(message.chat.id, mes + link_mes, reply_markup=keyboard, parse_mode='Markdown')
        help_mes = 'Если не нашли подходящей должности, вы можете просто прислать ваше резюме на почту hr@korablik-fond.ru' + \
                   ' или присоединиться к волонтерской программе. Мы рады всем!'
        await bot.send_message(message.chat.id, help_mes, parse_mode='Markdown')
        await bot.send_message(message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)

    # #   Кнопка управления подпиской
    elif message.text[0:10].lower() == 'управление':
        if not db.subscriber_exist(message.from_user.id):
            await bot.send_message(message.chat.id, 'Вы не подписаны! Хотите подписаться?',
                                   reply_markup=subscription_keyboard)
        else:
            await bot.send_message(message.chat.id, 'Вы уже подписаны! Желаете отписаться..?',
                                   reply_markup=unsubscription_keyboard)

    # #   Кнопка "Назад"
    elif message.text[0:5].lower() == 'назад':
        await bot.send_message(message.chat.id, RETURN_MESS.format(message.chat.first_name),
                               reply_markup=start_markup, parse_mode='Markdown')

    # #   Неизвестная команда
    else:
        try:
            await bot.send_message(message.chat.id, 'Простите, я не знаю такой команды ' +
                                   emoji.emojize(':pensive_face:') + '\n*Попробуйте еще раз!*', parse_mode='Markdown')
        except Exception as err:
            print('Something wrong! Exception: {}'.format(err))


@dis.message_handler(content_types=['document'])
async def handle_doc(message):
    """ Обработчик резюме """
    doc_id = message.document.file_id
    doc_name = message.document.file_name
    try:
        file_info = await bot.get_file(doc_id)  # max 20 MB
        #   file.file_path = 'C:/Users/User/Documents/PycharmProjects/Korablik/'
        urllib.request.urlretrieve(f'http://api.telegram.org/file/bot{config.TOKEN}/{file_info.file_path}',
                                   f'./documents/{doc_name}')
        await bot.send_message(message.chat.id, 'Спасибо, ваше резюме принято!')
    except FileIsTooBig:
        error_mes = 'Файл слишкой большой. Максимальный допустимый размер - 20МБ\nПопробуйте загрузить другой файл'
        await bot.send_message(message.chat.id, error_mes)


@dis.callback_query_handler(lambda call: True)
async def subscription_command(call):
    """ Обработчик команд подписки/отписки """
    await bot.answer_callback_query(call.id)
    if call.data == 'yes':
        db.update_subscription(call.from_user.id, True)
        await bot.send_message(call.message.chat.id, 'Отлично! Вы подписаны.')
        await bot.send_message(call.message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)
    elif call.data == 'no':
        db.update_subscription(call.from_user.id, False)
        await bot.send_message(call.message.chat.id, 'Жаль... Вы не подписаны')
        await bot.send_message(call.message.chat.id, FEEDBACK_MESS, reply_markup=back_markup)


async def send_discribution():
    """ Рассылка новых детей всем подписчикам """
    while True:
        await asyncio.sleep(10)     # 10 секунд в тестовом режиме, 259200 (3*24*60*60) - 3 дня

        new_child = pars.new_child(pars.get_parser(BASE_HOST + CHILD_HOST).text)

        if new_child:
            subscribers = db.get_subscriptions()
            for dic in new_child:
                mes = '*' + str(dic['name']) + '*\n\n' + str(dic['age']) + '\n' + str(dic['city']) + \
                      '\n' + str(dic['diagnoz']) + '\n' + '\n_' + str(dic['money'] + '_')
                for sub in subscribers:
                    keyboard = InlineKeyboardMarkup()
                    keyboard.add(InlineKeyboardButton('Помочь прямо сейчас!',
                                                      url=str(dic['link']) + '&' + LINK_TRACK.format(
                                                          sub[1])))
                    await bot.send_photo(sub[1], str(dic['img']))
                    await bot.send_message(sub[1], mes +
                                           '\n\nДля более подробной информации перейдите по _ссылке_ на страничку ребенка.',
                                           reply_markup=keyboard, parse_mode='Markdown')


if __name__ == '__main__':
    loop.create_task(send_discribution())
    executor.start_polling(dis, skip_updates=True)
