from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint
from .views import TaskDefinitionView
from .models import TaskDefinition # Import your model

# Create a Flask Blueprint (optional, but good practice if you add custom static/template files)
task_config_bp = Blueprint(
    "task_config_bp",
    __name__,
    template_folder="templates",  # Create 'plugins/task_config_plugin/templates' if needed
    static_folder="static",    # Create 'plugins/task_config_plugin/static' if needed
    static_url_path="/static/task_config_plugin",
)

# Instantiate the ModelView
task_definition_view = TaskDefinitionView()
# task_definition_view.appbuilder_sm = None # Usually not needed, FAB handles security manager

# Define the plugin class
class TaskConfigPlugin(AirflowPlugin):
    name = "task_config_plugin"
    
    # Register the ModelView
    flask_appbuilder_views = [
        {
            "name": "Task Definitions", # Name of the menu item
            "category": "Task Configuration", # Category in the Airflow menu
            "view": task_definition_view,
        }
    ]
    
    # Register the Blueprint (if you have one)
    blueprints = [task_config_bp]
    
    # Register SQLAlchemy models
    # This is crucial for Airflow to recognize and manage the database table.
    models = [TaskDefinition]

    # Other plugin components (operators, hooks, etc.) can be added here if needed
    # operators = []
    # hooks = []
    # macros = []
    # admin_views = []
    # menu_items = []