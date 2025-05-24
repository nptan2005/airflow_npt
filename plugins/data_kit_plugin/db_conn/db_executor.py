from typing import Tuple,Optional,Dict
import inspect
from data_kit_plugin.db_conn.connConstant import ConnConstant
from data_kit_plugin.db_conn.db_hook_conn import DBHookConn
from data_kit_plugin.db_conn.orl_conn import OrlConn
import logging

class DBExecutor:
    def __init__(self, connection_type:str = ConnConstant.CONN_DB_HOOK):
        self.connection_type = connection_type
        if not connection_type:
            self.connection_type = ConnConstant.CONN_DB_HOOK
        else:
            self.connection_type = ConnConstant.CONN_DB_ORACLE
        self.logger = logging
        
    def __enter__(self):
        return self

    def __del__(self):
        del self.task
        del self.logger
        del self.connection_type

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.task = None
        self.logger = None
        self.connection_type = None
        
    def execute_procedure(self,connection:str, prc_name:str, params = None) -> bool:
        # Check if the script exists
        if self.connection_type == ConnConstant.CONN_DB_ORACLE:
            try:
                with OrlConn(connection_id=connection) as db:
                    db.execute_procedure(prc_name,params)
                return True
            except Exception as e:
                self.logger.exception(f"execute procedure = '{prc_name}, connection Str = {connection}, params = {params}' Error, {e}")
                return False
        else:
            try:
                with DBHookConn(connection_id=connection) as db:
                    db.execute_procedure(prc_name,params)
                return True
            except Exception as e:
                self.logger.exception(f"execute procedure = '{prc_name}, connection ID = {connection}, params = {params}' Error, {e}")
                return False
        
    # end execute_procedure
    
    
    def execute_procedure_out_param(self,connection:str, prc_name:str,params:list,out_params_type:dict)-> Tuple[bool,Optional[Dict]]:
        if self.connection_type == ConnConstant.CONN_DB_HOOK:
            return False,None
        # Check if the script exists
        if not out_params_type:
            return False, None
        if not connection or not prc_name:
            False, None
        out_results = None
        try:
            with OrlConn(connection) as db:
                out_results = db.execute_procedure_param(prc_name,params,out_params_type)
            return True,out_results
        except Exception as e:
            self.logger.exception(f"execute '{prc_name}' at connection Error, {e}")
            return False,out_results
    # end execute_cond_prc