import pandas as pd
from sqlalchemy import create_engine

def read_dataframe_from_sql(query, conn_string):
    engine = create_engine(conn_string)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df

def create_sample_dataframe():
    data = {'Column A': [1, 2, 3], 'Column B': ['A', 'B', 'C']}
    return pd.DataFrame(data)
