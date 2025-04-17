from airflow.plugins_manager import AirflowPlugin
from pd_to_excel_plugin.excel_export_operator import ExcelExportOperator

class ExcelExporterPlugin(AirflowPlugin):
    name = "excel_exporter_plugin"
    operators = [ExcelExportOperator]
