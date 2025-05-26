from airflow.plugins_manager import AirflowPlugin
from data_kit_plugin.export_operator import ExportOperator
from data_kit_plugin.excel_export_operator import ExcelExportOperator


class DataKitPlugin(AirflowPlugin):
    name = "data_kit_plugin"
    operators = [ExportOperator, ExcelExportOperator]
