# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint as pp

url = 'https://www.servplus.ru/service/'
# ur = 'https://www.servplus.ru/ajax/service.map/getElements.php?SECTION_ID=52&PARTNER_TYPE=service_center'
base_url = 'https://www.servplus.ru/ajax/service.map/getElements.php?SECTION_ID='
partner = '&PARTNER_TYPE=service_center'



def get_html(url):
    r = requests.get(url)
    return r.text

def get_cities(html):
    soup = bs(html,'lxml')
    cities = soup.find('select', class_='js-custom-select i-select').find_all('option')
    urls =[]
    for item in cities:
        urls.append(base_url + item.get('data-id') + partner)
    return urls

# <html><body><li data-baloon="Зарипов Фанис Газизович" data-coord="54.899984580316,52.294586579101" data-id="259">
# <div class="m-name">Зарипов Фанис Газизович (АСЦН)</div>
# <div class="m-status">Сервисный центр</div>
# <p>+7 (962) 553-4737</p>
# <p><a href="mailto:f.zaripov@ascn.ru">f.zaripov@ascn.ru</a></p>
# <p><a href="http://"></a></p>
# </li>
# </body></html>

def get_data(data):
    for item in data[1:2]:
        html = get_html(item)
        soup = bs(html,'lxml')
        coord = soup.find('li').get('data-coord')
        m_name = soup.find('div', class_='m-name').text
        phone = soup.find('div', class_='m-status').find_next().text
        mail = soup.find('a').text
        link = soup.find('a').find_next().text
        data_id = soup.find('li').get('data-id')
        # return soup
        print(data_id)

def main():
    cities = get_cities(get_html(url))
    data = get_data(cities)
    # print(data)

if __name__ == '__main__':
    main()
