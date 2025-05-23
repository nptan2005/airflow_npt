from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint

# from flask_appbuilder import BaseView, expose
from custom_config_plugin.views import AppSettingView
from custom_config_plugin.models import AppSetting  # Import your model

# Create a Flask Blueprint
custom_config_bp = Blueprint(
    "custom_config_bp",
    __name__,
    template_folder="templates",  # You can create a 'templates' subfolder for custom HTML
    static_folder="static",  # You can create a 'static' subfolder for CSS/JS
    static_url_path="/static/custom_config_plugin",  # URL path for static files
)

# If you wanted a completely custom page (not a ModelView)
# class MyCustomPageView(BaseView):
#     route_base = "/custom_config" # URL for this view
#
#     @expose("/") # Expose a method at the route_base
#     def list(self):
#         # You can query your AppSetting model here or do other logic
#         # settings = self.appbuilder.get_session.query(AppSetting).all()
#         # msg = f"Found {len(settings)} settings."
#         # return self.render_template("my_custom_page.html", content=msg) # Requires templates/my_custom_page.html
#         return "This is a custom page placeholder."

# Instantiate the ModelView for AppSettings
# app_settings_view = AppSettingView()
# flask_appbuilder_views = [
#     {
#         "name": "App Settings",
#         "category": "Custom Config",
#         "view": AppSettingView,
#     }
# ]

# app_settings_view.appbuilder_sm = (
#     None  # Reset SecurityManager if needed, usually handled by appbuilder
# )


# Define the plugin class
class CustomConfigPlugin(AirflowPlugin):
    name = "custom_config_plugin"

    # A list of class(es) derived from BaseView
    flask_appbuilder_views = [
        {
            "name": "App Settings",  # Name of the menu item
            "category": "Custom Config",  # Category in the menu
            "view": AppSettingView,
        }
        # If you had a custom page:
        # {
        #     "name": "My Custom Page",
        #     "category": "Custom Config",
        #     "view": MyCustomPageView(),
        # }
    ]

    # A list of blueprint object(s)
    blueprints = [custom_config_bp]

    # A list of menu item(s)
    # menu_items = [] # You can also define menu items directly here
    menu_links = [
        {
            "name": "Custom Config",
            "href": "/app/custom_config_plugin/appsettingview/list/",
            "category": "Custom Plugins",
        }
    ]

    # A list of SQLAlchemy models that should be exposed to the ORM
    # This is important for Airflow to recognize and create/manage your table
    models = [AppSetting]

    # Other plugin components can be added here:
    # operators = []
    # sensors = []
    # hooks = []
    # executors = []
    # macros = []
    # admin_views = []
    # flask_blueprints = []
    # global_operator_extra_links = []
    # operator_extra_links = []
    # source_versions = []
