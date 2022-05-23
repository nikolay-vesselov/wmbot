from time import sleep
import xml.etree.ElementTree as ET
import requests
from interfaces import ApiInterface, WMProAuthInterface, TestWMSigner
import time
#import interfaces

api = ApiInterface(WMProAuthInterface("276752932432", "kickkick", "/home/ubuntu/wmkeys/276752932432.kwm"))

res = api.x8(purse="R328079907035", reqn=int(time.time()))#["response"]["wmid"]["text"]

print(res)


def get_rate(data_of_my_order, type, red_rate, red_limit, delta, sum_for_down):
    print(data_of_my_order)
    i = 0
    my_position = 0


id = '77207708'
type = 'sellwmx'
redLimit = 10
redRate = 35.4
sum_for_down = 0.1
delta = 0.002


url = 'https://wm.exchanger.ru/asp/XMLWMList.asp?exchtype=34'
root = ET.fromstring(requests.get(url).content)
my_order = dict();
i: int = 0
my_position = 0
needed = 0
rate_to_set = 0
for child in root[1]:
    i = i + 1
    #print(child.tag, child.attrib['id'])
    if child.attrib['id'] == id:
        my_position = i
        print('Найдена моя заявка, пропускаем цикл')
        my_order['id'] = child.attrib['id']
        my_order['amount_wmx'] = child.attrib['amountin'].replace(',', '.')
        my_order['amount_wmz'] = float(child.attrib['amountout'].replace(',', '.'))
        my_order['rate'] = float(child.attrib['outinrate'].replace(',', '.'))
        continue

    if type == 'sellwmx':
        if float(child.attrib['amountout'].replace(',', '.')) > redLimit and redRate <= float(child.attrib['outinrate'].replace(',', '.')):
            print('yes - ', child.attrib['id'], " - ", child.attrib['outinrate'])
            if my_position == 0:
                needed = 1
                rate_to_set = float(child.attrib['outinrate'].replace(',', '.')) - delta
                print('Условие 1: Не нашел позицию моего ордера, но нашел конкурента')


            if my_position > 0 and float(child.attrib['outinrate'].replace(',', '.')) - my_order['rate'] > sum_for_down:
                needed = 1
                rate_to_set = float(child.attrib['outinrate'].replace(',', '.')) - delta
                print('Условие 2: Нашел позицию моего ордера и он значительно выше ближ конкурента. Опускаем курс...')

            if needed == 1:
                break



        else:
            print('no - ', child.attrib['id'], " - ", child.attrib['outinrate'])


#get_rate(data_of_my_order, 1, 1, 1, 1, 1)
print(my_order)

unittest.main()
 