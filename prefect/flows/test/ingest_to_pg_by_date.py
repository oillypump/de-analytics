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


@task(name="read_data", log_prints=True)
def read_data(path: Path) -> pd.DataFrame:
    df = pd.read_parquet(path)
    print(f"path file :\n{path}")

    # cek is null column
    isnul = df.isnull().any()
    print(f"check null :\n{isnul}")
    print(f"column yang memiliki nilai null :\n{isnul}")

    # convert as datetime column waktu_post
    df['waktu_post'] = pd.to_datetime(df['waktu_post'])

    #
    print(f"\n")
    print(f"jumlah row count :\n{len(df)}")

    # drop duplicates
    df = df.drop_duplicates(subset=['generated_id'], keep="first")

    print(f"jumlah row count :\n{len(df)}")

    # sort by datetime and and column keyword search
    df = df.sort_values(by='waktu_post')
    df['keyword'] = "pemilu 2024"

    print(f" data from gbucket: \n{df}")
    print(f"print type column :\n{df.dtypes}")

    return df


@task(log_prints=True, retries=3)
def insert_to_pg(table_name, df):

    sql_query = f'''
        SELECT generated_id
        FROM {table_name}
    '''

    database_block = SqlAlchemyConnector.load("postgres-connect")
    with database_block.get_connection(begin=False) as engine:

        existing_data = []
        try:
            existing_data = pd.read_sql(sql_query, con=engine)

            print(f"existing data : \n{existing_data}")
            print(f"jumlah row count :\n{len(existing_data)}")
        except psycopg2.errors.UndefinedTable:
            print("table not exist : dari psycopg2 errors")
        except sqlalchemy.exc.ProgrammingError:
            print("table not exist: dari sqlalchemy")

        if len(existing_data) > 1:
            
            df = df[~df['generated_id'].isin(existing_data['generated_id'])]
            
            print(f"drop duplicate dataframe : \n{df}")


            df = df.reset_index(drop=True)
            df = df.set_index('generated_id')
            print(f"reset index dataframe : \n{df}")

            if len(df) > 0:
                print("insert new record")
                df.to_sql(name=table_name, con=engine, if_exists='append')
            else: 
                print(f"no new record")

        else:
            
            print(f"no existing table")
            df = df.reset_index(drop=True)
            df = df.set_index('generated_id')

            df.head(n=0).to_sql(name=table_name, con=engine, if_exists="replace")
            df.to_sql(name=table_name, con=engine, if_exists='append')


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
    date = 27
    month = 3
    year = 2023
    
    path = download_from_bucket(date, month, year)

    """2. transform"""
    data = read_data(path)

    """3. truncate insert to table"""
    insert_to_pg("detik_table", data)

    """4. remove_file"""
    delete_file(path)


if __name__ == "__main__":
    ingest_to_pg()
