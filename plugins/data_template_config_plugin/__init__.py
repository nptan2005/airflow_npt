from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint
from data_template_config_plugin.models import (
    DBImportTemplate,
    DBExportTemplate,
    DBExportSheetConfig,
)

# Create a Flask Blueprint (optional, but good practice)
data_template_config_bp = Blueprint(
    "data_template_config_bp",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/static/data_template_config_plugin",
)


# Đăng ký plugin class
class DataTemplateConfigPlugin(AirflowPlugin):
    name = "data_template_config_plugin"

    # Register ModelViews (chỉ đăng ký class)
    flask_appbuilder_views = [
        {
            "name": "Import Templates",
            "category": "Data Templates",
            "view": "data_template_config_plugin.views.DBImportTemplateView",
        },
        {
            "name": "Export Templates",
            "category": "Data Templates",
            "view": "data_template_config_plugin.views.DBExportTemplateView",
        },
    ]

    blueprints = [data_template_config_bp]
    models = [DBImportTemplate, DBExportTemplate, DBExportSheetConfig]
