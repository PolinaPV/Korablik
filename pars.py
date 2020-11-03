import requests
from bs4 import BeautifulSoup


HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'
}


def get_html(url):
    req = requests.get(url, headers=HEADERS)
    return req


def get_parser(url):
    html = get_html(url)
    if html.status_code == 200:
        return html
    else:
        print('Error status code')


def get_all_content(url):
    soup = BeautifulSoup(url, 'html5lib')
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


def get_child(url, num):
    child = get_all_content(url.text)
    print(child[num - 1])


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


def get_memo(url):
    soup = BeautifulSoup(url, 'html5lib')
    lead = soup.find('p', class_='lead')
    spisok = soup.find('ul', class_='mb-4')
    info = dict({
        'lead': lead.get_text(),
        'spisok': spisok.get_text()
    })
    return info


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
