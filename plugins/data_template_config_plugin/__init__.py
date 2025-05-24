from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint
from data_template_config_plugin.views import DBImportTemplateView, DBExportTemplateView
from data_template_config_plugin.models import (
    DBImportTemplate,
    DBExportTemplate,
    DBExportSheetConfig,
)

# Create a Flask Blueprint (optional, but good practice)
data_template_config_bp = Blueprint(
    "data_template_config_bp",
    __name__,
    template_folder="templates",  # Create 'plugins/data_template_config_plugin/templates' if needed
    static_folder="static",  # Create 'plugins/data_template_config_plugin/static' if needed
    static_url_path="/static/data_template_config_plugin",
)

# Instantiate views
db_import_template_view = DBImportTemplateView()
db_export_template_view = DBExportTemplateView()
# DBExportSheetConfigViewInline is handled by its relation in DBExportTemplateView


# Define the plugin class
class DataTemplateConfigPlugin(AirflowPlugin):
    name = "data_template_config_plugin"

    # Register ModelViews
    flask_appbuilder_views = [
        {
            "name": "Import Templates",
            "category": "Data Templates",  # Menu category
            "view": db_import_template_view,
        },
        {
            "name": "Export Templates",
            "category": "Data Templates",
            "view": db_export_template_view,
        },
    ]

    # Register the Blueprint
    blueprints = [data_template_config_bp]

    # Register SQLAlchemy models
    # This is crucial for Airflow to recognize and manage the database tables.
    models = [DBImportTemplate, DBExportTemplate, DBExportSheetConfig]

    # Other plugin components (operators, hooks, etc.) can be added here if needed
