import requests
from bs4 import BeautifulSoup as bs
import csv
import base64
from datetime import datetime

key = 'pemilu+2024'
now = datetime.now()
date = now.strftime("%d/%m/%Y")

# url = 'https://www.detik.com/search/searchall?query={}&sortby=time&page='.format(key)

url = f'https://www.detik.com/search/searchall?query={key}&sortby=time&sorttime=0&fromdatex={date}&todatex={date}&siteid=2'

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'
}

datas = []

req = requests.get(url, headers=headers)

soup = bs(req.text, 'html.parser')
items = soup.findAll('article')

for i in items:
    link_url = i.find('a')['href']
    name = i.find('h2', 'title').text
    waktu_post = i.find('span', 'date').text.replace(
        'WIB', '').split(',')[1]
    category = i.find('span', 'category').text

    req_ = requests.get(link_url, headers=headers)
    soup_ = bs(req_.text, 'html.parser')
    author = soup_.find('div', 'detail__author').text.split('-')[0]
    content = soup_.findAll('div', 'detail__body itp_bodycontent')

    # for x in content:
    #     x = x.find_all('p')
    #     y = [y.text for y in x]
    #     content_ = ''.join(y).replace('\r\n', " ").replace(
    #         'ADVERTISEMENT', '').replace('SCROLL TO CONTINUE WITH CONTENT', '').replace('                            ', ' ').replace('[Gambas:Video 20detik]', '')

    unique_id = name
    unique_id_bytes = unique_id.encode("ascii")
    base64_bytes = base64.b64encode(unique_id_bytes)
    generated_id = base64_bytes.decode("ascii")

    print(generated_id, '||', name, '||', link_url,
          '||', category, '||', author, '||', waktu_post)

    # datas.append(
    #     [link_url, name, author, waktu_post, category, content_])

# csv_headers = ['link_url', 'Headline', 'Author',
#                'waktu_post', 'category', 'content']
# writer = csv.writer(
#     open('results/pemilu.csv', 'w', encoding='utf8',  newline=''))
# writer.writerow(csv_headers)
# for d in datas:
#     writer.writerow(d)
