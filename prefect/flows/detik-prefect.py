from prefect import flow, task
import requests
from bs4 import BeautifulSoup as bs
import base64
import pandas as pd
from datetime import datetime
from pathlib import Path
from prefect_gcp.cloud_storage import GcsBucket
import os


@task(name="Crawl Task", log_prints=True)
def scrap_task(url: str, key: str, headers: str) -> None:

    datas = []

    req = requests.get(url, headers=headers)

    soup = bs(req.text, 'html.parser')
    items = soup.findAll('article')

    for i in items:
        link_url = i.find('a')['href']
        name = i.find('h2', 'title').text
        waktu_post = i.find('span', 'date').text.replace('WIB', '').split(',')[1]
        category = i.find('span', 'category').text

        req_ = requests.get(link_url, headers=headers)
        soup_ = bs(req_.text, 'html.parser')
        content = soup_.findAll('div', 'detail__body itp_bodycontent')

        for x in content:
            author = soup_.find('div', 'detail__author').text.split('-')[0]

            unique_id = name
            unique_id_bytes = unique_id.encode("ascii")
            base64_bytes = base64.b64encode(unique_id_bytes)
            generated_id = base64_bytes.decode("ascii")

            datas.append([generated_id, name, link_url, author, waktu_post, category])
    
    df = pd.DataFrame.from_dict(datas)

    return df

@task(name="Transform", log_prints=True)
def transform_data(df):

    column_names = ["generated_id", "name", "link_url", "author", "waktu_post", "category"]
    df.columns = column_names
    print(f"columns :{df.dtypes}")
    return df

@task(name="Write Local", log_prints=True)
def write_local(df: pd.DataFrame, dataset_file: str):
    
    path = Path(f"data/{dataset_file}.parquet")
    if path.is_file() == True:
        df_before = pd.read_parquet(f"{path}")
        df_new = pd.concat([df_before, df])
        df_new.to_parquet(path, compression="gzip")
        print(df_new)
        print('this is concat cases')
    else:
        df.to_parquet(path, compression="gzip")
        print('this is write new')
    
    return path

@task()
def write_gcs(path: Path) -> None:
    """upload parquet to GCS"""
    gcs_block = GcsBucket.load("bucket-google")
    gcs_block.upload_from_path(
        from_path=f"{path}",
        to_path=path
    )
    """remove existing data on file system"""
    # cmd =F"rm {path}"
    # os.system(cmd)

@flow(name="Scrap Flow", log_prints=True)
def main_flow():

    """1. flow scrap"""
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36'}

    key = 'pemilu+2024'
    now = datetime.now()
    date = now.strftime("%d/%m/%Y")  # dd/mm/yyyy

    url = f"https://www.detik.com/search/searchall?query={key}&sortby=time&sorttime=0&fromdatex={date}&todatex={date}&siteid=2"

    raw_data = scrap_task(url, key, headers)

    """2. transform data/give header column"""
    df = transform_data(raw_data)

    """3. write to local"""
    # dataset_date = now.strftime("%d_%m_%Y_%H_%M_%S")
    dataset_date = now.strftime("%d_%m_%Y")
    dataset_file = f"detik_{dataset_date}"
    path = write_local(df, dataset_file)

    """4. write to gcs"""
    write_gcs(path)


if __name__ == '__main__':
    main_flow()
