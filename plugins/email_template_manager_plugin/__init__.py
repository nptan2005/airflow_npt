from airflow.plugins_manager import AirflowPlugin
from flask import Blueprint
from email_template_manager_plugin.views import DBEmailTemplateView
from email_template_manager_plugin.models import DBEmailTemplate

# Tạo Flask Blueprint (tùy chọn, nhưng tốt nếu bạn có file static/template tùy chỉnh)
email_template_manager_bp = Blueprint(
    "email_template_manager_bp",
    __name__,
    template_folder="templates",  # Trỏ đến 'plugins/email_template_manager_plugin/templates' nếu có
    static_folder="static",  # Trỏ đến 'plugins/email_template_manager_plugin/static' nếu có
    static_url_path="/static/email_template_manager_plugin",
)

# Khởi tạo view
db_email_template_view = DBEmailTemplateView()


# Định nghĩa class plugin
class EmailTemplateManagerPlugin(AirflowPlugin):
    name = "email_template_manager_plugin"

    # Đăng ký ModelView
    flask_appbuilder_views = [
        {
            "name": "Email Templates",  # Tên mục menu
            "category": "Email Management",  # Danh mục trong menu Airflow
            "view": db_email_template_view,
        }
    ]

    # Đăng ký Blueprint
    blueprints = [email_template_manager_bp]

    # Đăng ký SQLAlchemy models
    # Quan trọng để Airflow nhận diện và quản lý bảng CSDL.
    models = [DBEmailTemplate]

    # Các thành phần plugin khác (operators, hooks, etc.) có thể thêm ở đây nếu cần
