import requests
import time
from bs4 import BeautifulSoup as BS
import codecs

url = "https://nic.kz/"

with codecs.open("new_domain.txt", 'r', "utf-8") as file:
    arr_domains = [row.strip() for row in file]

for i in range(len(arr_domains)):
    #print(arr_domains[i])
    i += i

print("===========================\n")

q = 0

while q < 2000:
    i = 0
    response = requests.get(url)
    soup = BS(response.text, 'lxml')
    quotes = soup.find('table', {'id': 'last-ten-table'}).findChildren()[3].text

    new_domains_from_nic = []
    new_domains_from_nic = quotes.split('\n')
    #print(type(new_domains_from_nic))

    file_w = codecs.open("new_domain.txt", 'a', "utf-8")

    while i < len(new_domains_from_nic):
        if new_domains_from_nic[i] == '':
            i += 1
            continue
        else:
            res = new_domains_from_nic[i].split('2022')
            #print(res[1])

            if i == len(new_domains_from_nic)-1:
                break

            if res[1] in arr_domains:
                print(f"{i} - Have in arr_domains...")
                i += 1
                continue

            else:
                print("New domain in list...***")
                arr_domains.append(res[1])


                file_w.write(f"{res[1]}\n")
                i += 1

    q += 1
    print('sleep 3 min...')
    file_w.close()
    time.sleep(180)

