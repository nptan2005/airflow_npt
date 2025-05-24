from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint, render_template
from airflow.models import BaseOperator

# Tạo Flask Blueprint để phục vụ giao diện web
custom_plugin_bp = Blueprint(
    "custom_plugin_bp",  # Tên Blueprint
    __name__,
    template_folder="templates",  # Thư mục chứa HTML template
    static_folder="static",       # Thư mục chứa file tĩnh như CSS/JS
)

@custom_plugin_bp.route("/custom_tab")
def custom_tab():
    return render_template("custom_tab.html")

# Định nghĩa một Operator tùy chỉnh
class MyCustomOperator(BaseOperator):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

    def execute(self, context):
        print(f"Hello {self.name} from MyCustomOperator!")

# Định nghĩa Plugin
class CustomPlugin(AirflowPlugin):
    name = "custom_plugin"
    flask_blueprints = [custom_plugin_bp]
    menu_links = [
        {
            "name": "Custom Tab",       # Tên hiển thị trên menu
            "href": "/custom_tab",      # URL của tab
            "category": "Custom Plugins"  # Nhóm trong menu
        }
    ]


