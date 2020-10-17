import requests
from bs4 import BeautifulSoup
import unicodecsv as csv

#   CSV = 'Childrens.csv'
HOST = 'https://korablik-fond.ru/'
URL_O = 'https://korablik-fond.ru/our-children/'
URL_C = 'https://korablik-fond.ru/contacts/'
URL_R = 'https://korablik-fond.ru/reporting/'
URL_A = 'https://korablik-fond.ru/about/S'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    #   print(type(r))
    return r


def get_all_content(html):
    soup = BeautifulSoup(html, 'html5lib')
    #   pg = soup.find('div', id='panel-689-1-0-2')  # Панель "Им нужна помощь"
    items = soup.find('div', id='panel-689-1-0-2').find_all('div', class_='child-card-content')
    child = []
    #   print(pg.prettify())
    for it in items:
        child.append(
            {
                'name': it.find('h4').get_text(strip=True),
                'info': [p.get_text(strip=True) for p in it.findAll('p')],  # it.find('p').get_text(),
                'link': HOST + it.find('div', class_='leyka-scale-button').find('a').get('href'),
                'money': [div.get_text() for div in it.findAll('div', class_='leyka-scale-label')]
                # it.find('div', class_='leyka-scale-label'),
                # 'img': HOST + it.find('div', class_='tpl-pictured-bg').get('style')
            }
        )
    return child


"""def save_data(items, path):   # Запись данных в csv файл, пока не работает :/
    with open(path, mode='w+', newline='', encoding='utf-8') as file:
        #   colum = ['Имя ребёнка', 'Информация', 'Ссылка', 'Собрано средства']
        writer = csv.writer(file, delimiter=';')     #  , lineterminator='\r', fieldnames=colum)
        #   writer.writeheader()
        #   writer.writerow(['Имя ребёнка', 'Информация', 'Ссылка', 'Собрано средства'])
        for item in items:
            writer.writerow([item.__str__('name'), item.__str__('info'), item.__str__('link'), item.__str__('money')])
"""


def get_child(url, num):
    n = parser(url)
    #   count = len(n)
    #   print(type(n))
    print(n[num-1])


def get_contacts(url):
    sp = BeautifulSoup(url, 'html5lib')
    cont = sp.find('div', class_='col-md-7').find('ul')
    # print(cont)
    tmp = cont.findAll('li')
    #   print(len(tmp))
    phone = tmp[0].find('span').get_text() + tmp[0].find('a').get('href'),
    mail = tmp[1].find('span').get_text() + tmp[1].find('a').get('href'),
    adress = tmp[2].find('span').get_text() + tmp[2].find('a').get('href')
    print('\t', phone, '\n\t', mail, '\n\t', adress)


def get_reports(url):
    print('COme soon!')


def get_about(url):
    print('COme soon!')


def parser(url, params=''):
    #html = get_html(URL_O)
    #if html.status_code == 200:
    child = []
    child.extend(get_all_content(url.text))
        #   save_data(child, CSV)
        #   print(child)
    #else:
    #    print('Error')
    return child


def info():
    print('\tЭлементы меню:\n'
          '\t i. Информация о меню\n'
          '\t 1. Вывод всех детей\n'
          '\t 2. Вывод n-ого ребёнка\n'
          '\t 3. Контакты\n'
          '\t 4. Отчеты\n'
          '\t 5. About us!\n'
          '\t 0. Exit.')


def menu():
    case = input('\tВыберете пункт меню: ')
    # case = int(case.strip())
    if case == '1':
        html = get_html(URL_O)
        if html.status_code == 200:
            print('\n'.join(map(str, parser(html))))
        else:
            print('Error status code')
    elif case == '2':
        choose = input('\tВыберете номер ребёнка: ')
        choose = int(choose.strip())
        html = get_html(URL_O)
        if html.status_code == 200:
            get_child(html, choose)
        else:
            print('Error status code')
    elif case == '3':
        r = get_html(URL_C)

        if r.status_code == 200:
            html = r.content
            get_contacts(html)
        else:
            print('Error status code')
        #   print(parser())
    elif case == '4':
        html = get_html(URL_R)
        if html.status_code == 200:
            get_reports(html)
        else:
            print('Error status code')
    elif case == '5':
        html = get_html(URL_A)
        if html.status_code == 200:
            get_about(html)
        else:
            print('Error status code')
    elif case == 'i':
        info()
        menu()
    elif case == '0':
        exit()
    else:
        print('Error case. Try again!')
        menu()
    menu()

def main():
    info()
    menu()
    """case = input('\tВыберете пункт меню: ')
    case = int(case.strip())
    if case == 1:
        html = get_html(URL_O)
        if html.status_code == 200:
            print(parser(html))
        else:
            print('Error status code')
    elif case == 2:
        choose = input('\tВыберете номер ребёнка: ')
        choose = int(choose.strip())
        html = get_html(URL_O)
        if html.status_code == 200:
            get_child(html, choose)
        else:
            print('Error status code')
    elif case == 3:
        r = get_html(URL_C)

        if r.status_code == 200:
            html = r.content
            get_contacts(html)
        else:
            print('Error status code')
        #   print(parser())
    elif case == 4:
        html = get_html(URL_R)
        if html.status_code == 200:
            get_reports(html)
        else:
            print('Error status code')
    elif case == 5:
        html = get_html(URL_A)
        if html.status_code == 200:
            get_about(html)
        else:
            print('Error status code')
    elif case == 0:
        return
"""

if __name__ == '__main__':
    main()
