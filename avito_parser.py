import requests
from bs4 import BeautifulSoup
from consts import DATE, ITEM_TABLES, TITLE, URL, PRICE, PROXY

from time import time, ctime
from random import choice


class Item:
    def __init__(self, title, url, price):
        self.title = title
        self.url = 'avito.ru' + url
        self.price = price


class Parser:
    def __init__(self):
        self.proxy = {"http": PROXY}
        


    def request(self, url):
        USER_AGENTS = [

            # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
            # 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36 OPR/74.0.3911.107',

            # 'Mozilla/5.0 (iPod; CPU iPhone OS 14_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1',
            # 'Mozilla/5.0 (Linux; Android 10; SM-N960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36',
            # 'Mozilla/5.0 (Linux; Android 10; LM-Q710(FGN)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.181 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36'
        ]
        self.headers = {'user-agent': choice(USER_AGENTS), 'accept': '*/*'}
        #print(self.headers)
        try:
            r = requests.get(url, headers=self.headers)
        except requests.exceptions.ConnectionError:
            print('ConnectionError')
        #r = requests.get(url, headers=self.headers, proxies=self.proxy)

        if r.status_code == 200:
            #print(ctime(time()), url)
            return r.text
        else:
            print(ctime(time()), r.status_code, r.reason)
            return False

    def check_if_url_is_correct(self, url):
        url = url.replace("m.", "")

        source = self.request(url)
        try:
            if source != None:
                soup = BeautifulSoup(source, "lxml")
                item_tables = soup.findAll('div', {'class': ITEM_TABLES})
        except Exception as e:
            print(e)
            return False
        if len(item_tables) > 0:
            return True
        else:
            return False

    def update_data(self, url, new_items=True):
        url = "https://www." + url
        #source = requests.get(url, headers=self.headers, proxies=self.proxy).text
        items = []
        source = self.request(url)
        if source != False:
            soup = BeautifulSoup(source, "lxml")
            item_tables = soup.findAll('div', {'class': ITEM_TABLES})
            print(ctime(time()), url, len(item_tables))
            for item_table in item_tables:
                #date = item_table.find('div', {'class': "snippet-date-info"}).attrs['data-relative'].split()
                try: date = item_table.find('div', {'class': DATE}).text.split()
                except Exception as e: 
                    #print(e)
                    continue
                #if True:
                title = item_table.find('h3', {'class': TITLE}).text.replace("\n", "")
                url = item_table.find('a', {'class': URL}).get('href').replace("\n", "")
                price = item_table.find('span', {'class': PRICE}).text
                if new_items:
                    #if date[0] == '1' and date[1] == 'минуту':
                    if (date[0] == 'Несколько' and date[1] == 'секунд') or (date[0] == '1' and date[1] == 'минуту'):
                        items.append(Item(title, url, price))
                else: 
                    items.append(Item(title, url, price))

            # if new_items:
            #     if len(items) > 1: result = f"Новых объявлений: {len(items)}\n"

            # count = 0
            # for item in items:
            #     if count < 20:
            #         result += item.price + " " + item.title+ "\n" + item.url + "\n\n"
            #         count += 1
            #     elif count < 40:
            #         result2 += item.price + " " + item.title+ "\n" + item.url + "\n\n"
            #         count += 1
            # return result, result2, len(items)
        return items


p = Parser()
#items = p.update_data('avito.ru/moskva/tovary_dlya_kompyutera/komplektuyuschie-ASgBAgICAUTGB~pm?cd=1&q=z490')

items = p.update_data('avito.ru/moskva/telefony?cd=1')
#items = p.update_data('google.com')



print(len(items))
del items, p