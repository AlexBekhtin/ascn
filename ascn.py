# coding=utf-8
import csv

import requests
from bs4 import BeautifulSoup
from urls import *


def get_html(url):
    r = requests.get(url)
    return r.text


def get_cities(html):
    soup = BeautifulSoup(html, 'lxml')
    cities = soup.find('select', class_='js-custom-select i-select').find_all('option')
    data = []
    for item in cities:
        data.append((item.text, int(item.get('data-id')), f"{base_url}{item.get('data-id')}{partner}"))
    return data


# <html><body><li data-baloon="Зарипов Фанис Газизович" data-coord="54.899984580316,52.294586579101" data-id="259">
# <div class="m-name">Зарипов Фанис Газизович (АСЦН)</div>
# <div class="m-status">Сервисный центр</div>
# <p>+7 (962) 553-4737</p>
# <p><a href="mailto:f.zaripov@ascn.ru">f.zaripov@ascn.ru</a></p>
# <p><a href="http://"></a></p>
# </li>
# </body></html>


def get_data(data):
    data_csv = []
    for item in data:
        html = get_html(item[2])
        soup = BeautifulSoup(html, 'lxml')
        lis = soup.find_all('li')
        for li in lis:
            try:
                city = item[0]
            except:
                city = ''
            try:
                city_id = item[1]
            except:
                city_id = ''
            try:
                coord = li.get('data-coord')
            except:
                coord = ''
            try:
                m_name = li.find('div', class_='m-name').text
            except:
                m_name = ''
            try:
                m_status = li.find('div', class_='m-status').text
            except:
                m_status = ''
            try:
                phone = li.find('div', class_='m-status').find_next().text
            except:
                phone = ''
            try:
                mail = li.find('a').text
            except:
                mail = ''
            try:
                link = li.find('a').find_next().text
            except:
                link = ''
            try:
                data_id = li.get('data-id')
            except:
                data_id = ''
            row = {'city': city,
                   'city_id': city_id,
                   'coord': coord,
                   'm_name': m_name,
                   'm_status': m_status,
                   'phone': phone,
                   'mail': mail,
                   'link': link,
                   'data_id': data_id}
            data_csv.append(row)
    return data_csv


def write_csv(data, file_name):
    field_names = data[0].keys()
    with open(file_name, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=field_names)
        writer.writeheader()
        for line in data:
            writer.writerow(line)


def main():
    cities = get_cities(get_html(url))
    data = get_data(cities)
    write_csv(data, 'ascn_partners.csv')


if __name__ == '__main__':
    main()
