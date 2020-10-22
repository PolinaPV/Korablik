import requests
from bs4 import BeautifulSoup
import json


BASE_HOST = 'https://korablik-fond.ru/'
CHILD_HOST = 'our-children/'
CONT_HOST = 'contacts/'
REP_HOST = 'reporting/'
ABOUT_HOST = 'about/'
HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url, headers=HEADERS, params=params)
    #   print(dir(r))
    return r


def get_all_content(html):
    soup = BeautifulSoup(html, 'html5lib')
    #   pg = soup.find('div', id='panel-689-1-0-2')  # Панель "Им нужна помощь"
    items = soup.find('div', id='panel-689-1-0-2').find_all('div', class_='child-card-content')
    child = []
    #   print(pg.prettify())
    for it in items:
        child.append(json.dumps(
            {
                'name': it.find('h4').get_text(strip=True),
                'info': [p.get_text(strip=True) for p in it.findAll('p')],  # it.find('p').get_text(),
                'link': BASE_HOST + it.find('div', class_='leyka-scale-button').find('a').get('href'),
                'money': [div.get_text() for div in it.findAll('div', class_='leyka-scale-label')]
                # 'img': HOST + it.find('div', class_='tpl-pictured-bg').get('style')
            }, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
        )
    return child


def get_child(url, num):
    n = parser(url)
    print(n[num-1])


def get_contacts(url):
    sp = BeautifulSoup(url, 'html5lib')
    cont = sp.find('div', class_='col-md-7').find('ul')
    # print(cont)
    tmp = cont.findAll('li')
    print(type(tmp))
    contact = json.dumps({
        'phone': tmp[0].find('span').get_text() + tmp[0].find('a').get('href'),
        'mail': tmp[1].find('span').get_text() + tmp[1].find('a').get('href'),
        'adres': tmp[2].find('span').get_text() + tmp[2].find('a').get('href')
    }, sort_keys=False, indent=4, ensure_ascii=False, separators=(',', ': '))
    print(contact)


def get_reports(url):
    print('COme soon!')


def get_about(url):
    print('COme soon!')


def parser(url, params=''):
    child = []
    child.extend(get_all_content(url.text))
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
        html = get_html(BASE_HOST+ CHILD_HOST)
        if html.status_code == 200:
            print('\n'.join(map(str, parser(html))))
        else:
            print('Error status code')
    elif case == '2':
        html = get_html(BASE_HOST + CHILD_HOST)
        if html.status_code == 200:
            patc = parser(html)
            length = len(patc)
            print('\tВыберете номер ребёнка (Available ', length, '):')
            choose = input()
            choose = int(choose.strip())
            get_child(html, choose)
        else:
            print('Error status code')
    elif case == '3':
        r = get_html(BASE_HOST + CONT_HOST)
        if r.status_code == 200:
            html = r.content
            get_contacts(html)
        else:
            print('Error status code')
        #   print(parser())
    elif case == '4':
        html = get_html(BASE_HOST + REP_HOST)
        if html.status_code == 200:
            get_reports(html)
        else:
            print('Error status code')
    elif case == '5':
        html = get_html(BASE_HOST + ABOUT_HOST)
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


if __name__ == '__main__':
    main()