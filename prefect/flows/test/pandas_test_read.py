import pandas as pd
from prefect import flow, task
from pathlib import Path
from prefect_gcp.cloud_storage import GcsBucket
from prefect_sqlalchemy import SqlAlchemyConnector
import psycopg2
import sqlalchemy

sql_query = f'''
        SELECT generated_id, author
        FROM test_table
    '''

database_block = SqlAlchemyConnector.load("postgres-connect")
with database_block.get_connection(begin=False) as engine:

        # existing_data = []
        try:
            existing_data = pd.read_sql(sql_query, con=engine)
            existing_data = existing_data.set_index('generated_id')
            
            print(f"existing data : \n{existing_data}")        
        except psycopg2.errors.UndefinedTable:
            print("table not exist : dari psycopg2 errors")
        except sqlalchemy.exc.ProgrammingError: 
            print("table not exist: dari sqlalchemy")
        
        