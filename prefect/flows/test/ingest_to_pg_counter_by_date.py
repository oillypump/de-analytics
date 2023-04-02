import pandas as pd
from prefect import flow, task
from pathlib import Path
from prefect_gcp.cloud_storage import GcsBucket
from prefect_sqlalchemy import SqlAlchemyConnector
import psycopg2
import sqlalchemy
from datetime import datetime


@task(name="download parquet from g bucket", log_prints=True)
def download_from_bucket(date: int, month: int, year: int) -> Path:
    """state directory target and source"""
    gcs_path = f"data/detik_{date}_{month:02}_{year}.parquet"
    gcs_block = GcsBucket.load("bucket-google")
    local_path_dir = f"/home/ubuntu/apps/de-analytics/prefect/flows/data_download/"
    """gcloud block script"""
    gcs_block.get_directory(
        from_path=gcs_path,
        local_path=local_path_dir
    )
    return Path(f"{local_path_dir}/{gcs_path}")


@task(name="read_data_scrap", log_prints=True)
def read_data(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    print(f"path file :\n{path}")

    # cek is null column
    isnul = df.isnull().any()
    print(f"check null :\n{isnul}")
    print(f"column yang memiliki nilai null :\n{isnul}")

    # convert as datetime column waktu_post
    df['waktu_post'] = pd.to_datetime(df['waktu_post'])

    print(f"\n")
    print(f"jumlah row count :\n{len(df)}")

    # drop duplicates
    df = df.drop_duplicates(subset=['generated_id'], keep="first")

    print(f"jumlah row count :\n{len(df)}")

    # sort by datetime and and column keyword search
    df = df.sort_values(by='waktu_post')
    df['keyword'] = "pemilu 2024"

    # print(f" data from gbucket: \n{df}")
    # print(f"print type column :\n{df.dtypes}")

    return df


@task(log_prints=True, name="read tokoh")
def read_tokoh() -> pd.DataFrame:

    sql_query = f'''
        SELECT nama_tokoh
        FROM popularitas_tokoh
    '''

    database_block = SqlAlchemyConnector.load("postgres-connect")
    with database_block.get_connection(begin=False) as engine:

        tokoh = pd.read_sql(sql_query, con=engine)
        tokoh = tokoh.to_dict("list")
        print(tokoh)

    return tokoh


@task(log_prints=True, retries=3)
def insert_to_pg(table_name, df, tokoh):

    # print(f" data from gbucket: \n{df}")
    # print(f" data tokoh dari sql: \n{tokoh}")

    paragraphs = df['name']

    words_to_count = tokoh['nama_tokoh']
    print(words_to_count)
    # words_to_count = ['prabowo', 'ahy']

    word_counts = {}

    for paragraph in paragraphs:
        # Convert the paragraph to lowercase and split it into words
        words = paragraph.lower().split()
        
        # Iterate over each word in the list of words
        for word in words:
            # If the word is in the list of words to count, increment its count
            if word in words_to_count:
                # If the word is already in the dictionary, increment its count
                if word in word_counts:
                    word_counts[word] += 1
                # If the word is not yet in the dictionary, add it with a count of 1
                else:
                    word_counts[word] = 1
                                
    # Create a DataFrame from the dictionary of word counts
    df_output = pd.DataFrame.from_dict(word_counts, orient='index', columns=['count'])

    # Sort the DataFrame by count in descending order
    df_output = df_output.sort_values('count', ascending=False)

    # Print the DataFrame
    print(f"\n {df_output}")


@task(log_prints=True)
def delete_file(path: Path):
    if path.is_file() == False:
        print('file already deleted')
    else:
        print("file existed")
        path.unlink()
        print("file successful deleted")


@flow(name="ingest flow", log_prints=True)
def ingest_to_pg():
    """1. download from gc bucket"""
    date = 29
    month = 3
    year = 2023

    path = download_from_bucket(date, month, year)

    """2. transform"""
    data_scrap = read_data(path)

    """2. sql data tokoh"""
    data_tokoh = read_tokoh()

    """3. truncate insert to table"""
    insert_to_pg("detik_table_counter", data_scrap, data_tokoh)

    """4. remove_file"""
    delete_file(path)


if __name__ == "__main__":
    ingest_to_pg()
