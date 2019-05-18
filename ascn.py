# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
import csv
from pprint import pprint as pp

url = 'https://www.servplus.ru/service/'
# ur = 'https://www.servplus.ru/ajax/service.map/getElements.php?SECTION_ID=49&PARTNER_TYPE=service_center'
base_url = 'https://www.servplus.ru/ajax/service.map/getElements.php?SECTION_ID='
partner = '&PARTNER_TYPE=service_center'



def get_html(url):
    r = requests.get(url)
    return r.text

def get_cities(html):
    soup = bs(html,'lxml')
    cities = soup.find('select', class_='js-custom-select i-select').find_all('option')
    data =[]
    for item in cities:
        data.append((item.text, int(item.get('data-id')),f"{base_url}{item.get('data-id')}{partner}"))
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
    for item in data:
        html = get_html(item[2])
        soup = bs(html,'lxml')
        try:
            city = item[0]
        except:
            city = ''
        try:
            city_id = item[1]
        except:
            city_id = ''
        try:
            coord = soup.find('li').get('data-coord')
        except:
            coord = ''
        try:
            m_name = soup.find('div', class_='m-name').text
        except:
            m_name = ''
        try:
            phone = soup.find('div', class_='m-status').find_next().text
        except:
            phone = ''
        try:
            mail = soup.find('a').text
        except:
            mail = ''
        try:
            link = soup.find('a').find_next().text
        except:
            link = ''
        try:
            data_id = soup.find('li').get('data-id')
        except:
            data_id = ''
        data ={'city':city,
               'city_id':city_id,
               'coord':coord,
               'm_name':m_name,
               'phone':phone,
               'mail':mail,
               'link':link,
               'data_id':data_id}
        write_csv(data,'ascn.csv')


def write_csv(line,file_name):
    with open(file_name, mode='a') as f:
        writer = csv.writer(f)
        writer.writerow((line['city'],
                         line['city_id'],
                         line['coord'],
                         line['m_name'],
                         line['phone'],
                         line['mail'],
                         line['link'],
                         line['data_id']))


def main():
    cities = get_cities(get_html(url))
    data = get_data(cities)


if __name__ == '__main__':
    main()
