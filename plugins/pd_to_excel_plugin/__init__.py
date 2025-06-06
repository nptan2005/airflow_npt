from airflow.plugins_manager import AirflowPlugin
from pd_to_excel_plugin.export_operator import ExportOperator

__all__ = ["ExportOperator"]  

class ExporterPlugin(AirflowPlugin):
    name = "exporter_plugin"
    operators = [ExportOperator]
