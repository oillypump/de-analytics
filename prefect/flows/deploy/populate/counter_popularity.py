import pandas as pd
from prefect import flow, task
from prefect_sqlalchemy import SqlAlchemyConnector


@task(log_prints=True, name="heading dan content")
def read_heading_content() -> pd.DataFrame:
    sql_query = f"""
        SELECT 
            name, 
            content
        FROM 
            detik_scrap_table
    """

    database_block = SqlAlchemyConnector.load("postgres-connect")
    with database_block.get_connection(begin=False) as engine:

        heading_content = pd.read_sql(sql_query, con=engine)

        heading_content['content'].fillna(
            heading_content['name'], inplace=True)
        heading_content['combined'] = heading_content['name'] + \
            ' ' + heading_content['content']


    return (heading_content)


@task(log_prints=True, name="read tokoh")
def read_tokoh() -> pd.DataFrame:

    sql_query = f"""
        SELECT nama_tokoh
        FROM tokoh_publik
    """

    database_block = SqlAlchemyConnector.load("postgres-connect")
    with database_block.get_connection(begin=False) as engine:

        tokoh = pd.read_sql(sql_query, con=engine)
        tokoh = tokoh.to_dict("list")

    return tokoh


@task(log_prints=True, retries=3)
def counter(heading_content, tokoh) -> pd.DataFrame:

    paragraphs = heading_content['combined']
    print(f"heading dan content :\n{heading_content}")

    words_to_count = tokoh['nama_tokoh']
    print(words_to_count)

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
    df_output = pd.DataFrame.from_dict(
        word_counts, orient='index', columns=['count'])

    # Sort the DataFrame by count in descending order
    df_output = df_output.sort_values('count', ascending=False)

    # Print the DataFrame
    print(f"\n {df_output}")
    return df_output


@task(log_prints=True, name="insert to db")
def insert_to_db(table_name, df_output):

    database_block = SqlAlchemyConnector.load("postgres-connect")
    with database_block.get_connection(begin=False) as engine:

        df_output.to_sql(name=table_name, con=engine, if_exists='replace')


@flow(name="Popularity Count V3", log_prints=True)
def popularity():
    """1. read to df, table detik_scrap column content and name"""
    heading_content = read_heading_content()

    """2. read to df, table tokoh """
    tokoh = read_tokoh()

    """3. count each tokoh"""
    df_output = counter(heading_content, tokoh)

    """4. write to df(df to sql)"""
    insert_to_db("tokoh_popularity", df_output)


if __name__ == "__main__":
    popularity()
