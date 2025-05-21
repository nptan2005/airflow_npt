import pandas as pd
import pandas.io.sql as psql
import logging

class DBHookConn:
    def __init__(self, connection_id: str, *args, **kwargs):
        """
        Initialize DatabaseHookWrapper using Airflow's BaseHook to fetch connection configuration.
        :param connection_id: The connection ID defined in Airflow connections.
        """
        self.connection_id = connection_id
        self.hook = None
        self._conn = None
        self._cursor
        self.logger = logging

        # Initialize connection
        self._initialize_hook()

    def _initialize_hook(self):
        """
        Initialize the hook based on the connection type.
        """
        try:
            self.hook = BaseHook.get_hook(self.connection_id)
            self._conn = self.hook.get_conn()  # This will return a connection object specific to the connection type
            self._cursor = self._conn.cursor()
        except Exception  as e:
            self.logger.exception(f'Error: {e}')
            self.__exit__

    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close
        self._clear_attributes()

    def __del__(self):
        self._clear_attributes()

    def _clear_attributes(self):
        """Clear object attributes during exit."""
        attributes = [
            '_conn', '_cursor', 
            'hook','logger']
        for attr in attributes:
            setattr(self, attr, None)
            
    @property
    def cursor(self):
        return self._cursor
    
    @property
    def fetchall(self):
        return self.cursor.fetchall()
    
    @property
    def fetch_all_df(self) -> pd.DataFrame:
        names = [ x[0] for x in self.cursor.description]
        rows = self.fetchall
        return pd.DataFrame( rows, columns=names)

    @property
    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None) -> pd.DataFrame:
        self.execute(sql, params or ())
        return self.fetchall()

    @property    
    def rows(self):
        return self.cursor.rowcount
    
    @property
    def connection(self):
        return self._conn
    
    @property
    def commit(self):
        self.connection.commit()

    @property
    def close(self):
        if self._cursor:
            self._cursor.close()
        if self._conn:
            self._conn.close()
    
    def execute_query(self, sql: str, params=None):
        """
        Execute a query on the database.
        """
        try:
            self.cursor.execute(sql, params or ())
            return self.cursor.fetchall()  # Return all rows
        except Exception as e:
            self.logger.exception(f"Error executing query: {e}")
            self.close


    def fetch_to_dataframe(self, sql: str, params=None) -> pd.DataFrame:
        """
        Fetch query result and convert to a pandas DataFrame.
        """
        try:
            self.cursor.execute(sql, params or ())
            rows = self.cursor.fetchall()
            columns = [desc[0] for desc in self.cursor.description]
            return pd.DataFrame(rows, columns=columns)
        except Exception as e:
            self.logger.exception(f"Error fetching data: {e}")
            self.close
        
    def execute(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
        except Exception  as e:
            self.logger.exception(e)
            self.close

    def split_schema_table(self,input_str):
            # Kiểm tra nếu có dấu chấm (.) trong chuỗi
            if '.' in input_str:
                schema_name, table_name = input_str.split('.', 1)  # Tách schema và table_name
                return schema_name, table_name
            else:
                # Nếu không có schema, chỉ có table_name
                return None, input_str
    # split_schema_table
        

    def execute_procedure(self, procedure, params = None):
        try:
            if params is None:
                self.cursor.callproc(procedure)
            else: 
                self.cursor.callproc(procedure,params)
        
        except Exception  as e:
            self.logger.exception(e)
            self.close 
    
    def tabel_to_df(self,tableName:str) -> pd.DataFrame:
        df = psql.read_sql_query(f"SELECT * FROM {tableName}", self.connection)
        return df
    
    def df_to_table(self, df: pd.DataFrame, tableName: str) -> bool:
        try:
            # Kiểm tra nếu DataFrame trống
            if df.empty:
                self._errorMsg = f"DataFrame is empty, no data to insert into {tableName}."
                return False

            # Ghi dữ liệu vào bảng
            df.to_sql(tableName, self.connection, if_exists='replace', index=False)

            # Kiểm tra số lượng bản ghi đã được chèn vào bảng
            query = f"SELECT COUNT(*) FROM {tableName}"
            result = pd.read_sql(query, self.connection)

            if result.iloc[0, 0] > 0:
                self._errorMsg = f"Data has been successfully inserted into {tableName}."
                return True
            else:
                self._errorMsg = f"Data insertion failed, no records found in {tableName}."
                return False

        except Exception as e:
            self.logger.exception(e)
            self.close
            return False
        
    # Đọc dữ liệu từ SQL bằng câu lệnh SQL
    def read_sql_query(self, sql_query: str, index_col=None, params=None) -> pd.DataFrame:
        """
        Executes an SQL query and returns the result as a DataFrame.

        :param sql_query: SQL query string to be executed.
        :param index_col: Column to set as index (optional).
        :param params: Parameters to pass to the SQL query (optional).
        :return: DataFrame containing the query result.
        """
        try:
            df = psql.read_sql_query(sql_query, self.connection, index_col=index_col, params=params)
            return df
        except Exception as e:
            self.logger.exception(e)
            self.close
            return None

    # Đọc dữ liệu từ một bảng SQL
    def read_sql_table(self, table_name: str, schema=None, index_col=None) -> pd.DataFrame:
        try:
            df = psql.read_sql_table(table_name, self.connection, schema=schema, index_col=index_col)
            return df
        except Exception as e:
            self.logger.exception(e)
            self.close
            return None

    # Đọc SQL (linh hoạt)
    def read_sql(self, sql: str, index_col=None) -> pd.DataFrame:
        try:
            df = psql.read_sql(sql, self.connection, index_col=index_col)
            return df
        except Exception as e:
            self.logger.exception(e)
            self.close
            return None

    # Ghi dữ liệu vào SQL
    def to_sql(self, df: pd.DataFrame, table_name: str, if_exists='replace', index=False):
        try:
            df.to_sql(table_name, self.connection, if_exists=if_exists, index=index)
            self._errorMsg = f"DataFrame successfully written to table: {table_name}"
        except ValueError as e:
            self.logger.exception(f"ValueError: {e}")
            self.close
            return False
        except Exception as e:
            self.logger.exception(f"Error writing DataFrame to table: {e}")
            self.close
            return False
        return True

    # Tạo câu lệnh CREATE TABLE từ DataFrame
    def pd_get_schema(self, df: pd.DataFrame, table_name: str, flavor=None) -> str:
        try:
            schema = psql.get_schema(df, table_name, con=self.connection, flavor=flavor)
            return schema
        except Exception as e:
            self.logger.exception(e)
            self.close
            return ""

    # Thực thi câu lệnh SQL trực tiếp
    def pd_execute(self, sql: str):
        try:
            psql.execute(sql, self.connection)
        except Exception as e:
            self.logger.exception(e)
            self.close


    def execute_script_list(self, script_list: list) -> list:
        dataArr = []
        # print(sriptArr)
        for i in range(len(script_list)):
            data = None
            # print(dataArr[i])
            self.execute(script_list[i])
            
            names = [ x[0] for x in self.cursor.description]
            rows = self.cursor.fetchall()

            data = pd.DataFrame( rows, columns=names)

            # print(data)

            dataArr.append(data)  
            data = None
            
        return dataArr
    
    def get_data_type_table(self, tableName:str) -> pd.DataFrame:
        """Get data Type from table"""
        df = pd.DataFrame()
        try:
            schema_name, table_name = self.split_schema_table(tableName)
            params = [table_name.upper()]
            df = self.execute_prc_with_cursor('bvbpks_schedule_api.pr_get_data_type',params)
        except Exception as e:
            self.logger.exception(e)
        return df
    
    def execute_import_data(self, sql:str, df:pd.DataFrame):
        try:
            records = df.to_dict("records")
            for record in records:
                for key, value in record.items():
                    if value is None or value == '<NULL>':
                        record[key] = None
                    else: 
                        record[key] = value
            self.cursor.executemany(sql, records)
        except Exception as e:
            self.logger.exception(f"Error import data to database {e}")
        finally:
            self.commit



    def schedule_process_data(self, sql:str, params) -> pd.DataFrame:
        self.execute(sql, params)
        return self.fetch_all_df


