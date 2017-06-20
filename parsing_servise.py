# -*- coding: utf-8 -*-

import requests
import re
import csv

from bs4 import BeautifulSoup
from time import sleep
from random import uniform


def get_html(url):
    """
    Response html page
    :param url: url page
    :return: html
    """
    r = requests.get(url)  # Response html

    return r.text


def get_links_all(html):
    """
    Page all links.
    :param html: html page
    :return: list links
    """
    soup = BeautifulSoup(html, 'lxml')
    all_li = soup.find('div', class_='pagepost').find_all('li', style="text-align: center;")

    links = [item.find('a').get('href') for item in all_li]

    return links


def write_csv(data, header):
    """
    Write file in csv.
    :param data: list
    :param header: list
    :return: file
    """

    with open('renault.cvs', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([header])
        for item in data:
            writer.writerow([item][0])


def get_address(html):
    """
    Get url. Search city, street, phone
    :param html: page html
    :return: list
    """
    soup = BeautifulSoup(html, 'lxml')
    page = soup.find('div', class_='pagepost')

    try:
        header = page.find('h1').text.strip()  # return header
    except AttributeError:
        print('Error Attribute "h1"')

    try:
        citys = page.find_all('h3')[0:-1]
    except AttributeError:
        print('Error Attribute "h3"')

    city = [item.text for item in citys]

    # Дополнительные города
    city_add = ['Московская область', 'Кемерово']
    city.extend(city_add)

    # search all street
    try:
        streets = page.find_all('p')
    except AttributeError:
        print('Error Attribute "p"')

    street = [i.text for i in streets][1:-1]

    # search all phone
    reg_phone = re.compile(r'[Тт]елефон.+\w?')

    # search index in str
    reg_index = re.compile(r'\d{6}?')

    # build the result
    arr = []
    for item in street:
        if reg_phone.findall(item):
            phone = '8' + item[11:]
            arr.append(phone)

        for i in city:
            if i in item:  # Search city
                if reg_index.search(item):
                    arr.append(i)
                    arr.append(item)
                    break

    result = [arr[i:i + 3] for i in range(0, len(arr), 3)]

    return result, header


def main():
    url = 'http://www.dusterauto.ru/spisok-oficialnyx-dilerov-renault'
    for html in get_links_all(get_html(url)):
        sleep(uniform(3, 6))

        result, header = get_address(get_html(html))
        write_csv(result, header)

        print('Parsing: {0}'.format(header))


if __name__ == '__main__':
    main()
