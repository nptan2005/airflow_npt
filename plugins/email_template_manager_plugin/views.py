from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from wtforms import TextAreaField  # Sử dụng TextAreaField cho nội dung HTML lớn
from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget  # Widget cho TextArea
from email_template_manager_plugin.models import DBEmailTemplate


class DBEmailTemplateView(ModelView):
    datamodel = SQLAInterface(DBEmailTemplate)

    list_title = "Email Templates"
    show_title = "Email Template Details"
    add_title = "Add New Email Template"
    edit_title = "Edit Email Template"

    list_columns = ["template_name", "subject", "description", "updated_at"]

    show_fieldsets = [
        ("Template Info", {"fields": ["template_name", "subject", "description"]}),
        ("Content", {"fields": ["body_html"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "expanded": False}),
    ]

    add_columns = ["template_name", "subject", "description", "body_html"]
    edit_columns = add_columns

    # Sử dụng TextAreaField cho body_html để dễ dàng nhập nội dung HTML dài
    form_overrides = {
        "body_html": TextAreaField,
    }
    # Cấu hình widget cho body_html để có kích thước lớn hơn
    form_widget_args = {
        "body_html": {
            "widget": BS3TextAreaFieldWidget(),  # Sử dụng widget chuẩn của FAB
            "rows": 20,  # Số dòng hiển thị
            "placeholder": "Nhập nội dung HTML của email template tại đây...",
        },
        "description": {"widget": BS3TextAreaFieldWidget(), "rows": 3},
    }

    label_columns = {
        "template_name": "Tên Template (Duy nhất)",
        "subject": "Chủ đề Email",
        "body_html": "Nội dung HTML",
        "description": "Mô tả",
        "created_at": "Ngày tạo",
        "updated_at": "Cập nhật lần cuối",
    }

    search_columns = ["template_name", "subject", "description", "body_html"]
    order_columns = ["template_name"]
