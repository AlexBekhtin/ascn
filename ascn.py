# coding=utf-8
import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint as pp

url = 'https://www.servplus.ru/service/'


def get_html(url):
    r = requests.get(url)
    return r.text

def get_cities(html):
    soup = bs(html,'lxml')
    cities = soup.find('select', class_='js-custom-select i-select').find_all('option')
    dt =[]
    for item in cities:
        dt.append((item.text, int(item.get('data-id'))))
    return print(dt)

def main():
     # print(get_html(url))
    get_cities(get_html(url))


if __name__ == '__main__':
    main()
