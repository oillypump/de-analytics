from prefect import flow, task
import requests
from bs4 import BeautifulSoup as bs
import base64
import pandas as pd
from datetime import datetime


@task(name="Crawl Task", log_prints=True)
def scrap_task(url: str, key: str, headers: str):

    datas = []
    for page in range(1, 2):

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

            unique_id = name
            unique_id_bytes = unique_id.encode("ascii")
            base64_bytes = base64.b64encode(unique_id_bytes)
            generated_id = base64_bytes.decode("ascii")

            print(generated_id, '||', name, '||', link_url,
                  '||', category, '||', author, '||', waktu_post)

            datas.append([generated_id, name, link_url,
                         author, waktu_post, category])

            # return datas
            # df = pd.DataFrame.from_dict(datas)
            # print(df)
            # print(f"columns: {df.dtypes}")
            # return df


@flow(name="Scrap Flow", log_prints=True)
def main_flow():


    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'}

    key = 'pemilu+2024'
    now = datetime.now()
    date = now.strftime("%d/%m/%Y") #dd/mm/yyyy
    print(date)
    # url = 'https://www.detik.com/search/searchall?query={}&sortby=time&page='.format(key)
    
    # url = f'https://www.detik.com/search/searchall?query={key}&sortby=time&page='
    
    url = f'https://www.detik.com/search/searchall?query={key}&sortby=time&sorttime=0&fromdatex={date}&todatex={date}&siteid=2'

    raw_data = scrap_task(url, key, headers)


if __name__ == '__main__':
    main_flow()
