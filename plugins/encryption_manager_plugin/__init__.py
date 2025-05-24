from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint
from encryption_manager_plugin.views import EncryptedDataRefView, EncryptDataView
from encryption_manager_plugin.models import EncryptedDataRef

# Create a Flask Blueprint for the plugin
encryption_manager_bp = Blueprint(
    "encryption_manager_bp",
    __name__,
    template_folder="templates",  # Points to 'plugins/encryption_manager_plugin/templates'
    static_folder="static",  # Create 'plugins/encryption_manager_plugin/static' if needed
    static_url_path="/static/encryption_manager_plugin",
)

# Instantiate views
encrypted_data_ref_view = EncryptedDataRefView()
encrypt_data_view = EncryptDataView()


# Define the plugin class
class EncryptionManagerPlugin(AirflowPlugin):
    name = "encryption_manager_plugin"

    # Register views
    flask_appbuilder_views = [
        {
            "name": "Encrypt New Data",  # Menu item for the custom encryption form
            "category": "Encryption Manager",  # Category in the Airflow menu
            "view": encrypt_data_view,
        },
        {
            "name": "View Encrypted Refs",  # Menu item for listing stored references
            "category": "Encryption Manager",
            "view": encrypted_data_ref_view,
        },
    ]

    # Register the Blueprint
    blueprints = [encryption_manager_bp]

    # Register SQLAlchemy models
    models = [EncryptedDataRef]

    # Other plugin components (operators, hooks, etc.) can be added here if needed
