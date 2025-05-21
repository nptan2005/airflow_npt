from airflow.plugins_manager import AirflowPlugin
from data_kit_plugin.export_operator import ExportOperator
from data_kit_plugin.db_conn.db_hook_conn import DBHookOperator
from data_kit_plugin.db_conn.orl_conn import OrlConnOperator
from data_kit_plugin.conn_kit.email_send_operator import EmailSendOperator
from data_kit_plugin.conn_kit.sftp_conn_operator import SftpConnOperator

class DataKitPlugin(AirflowPlugin):
    name = "data_kit_plugin"
    operators = [ExportOperator,DBHookOperator,OrlConnOperator,EmailSendOperator,SftpConnOperator]
