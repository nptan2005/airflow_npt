from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from custom_config_plugin.models import (
    AppSetting,
)  # Assuming models.py is in the same directory


class AppSettingView(ModelView):
    # def __init__(self):
    #     super().__init__()
    #     self.datamodel = SQLAInterface(
    #         AppSetting
    #     )  # ✅ Đảm bảo datamodel được khởi tạo đúng
    datamodel = SQLAInterface(AppSetting)

    # List view configuration
    list_columns = ["environment", "key", "value", "description", "updated_at"]
    list_title = "Application Settings"

    # Add/Edit view configuration
    add_columns = ["environment", "key", "value", "description"]
    edit_columns = ["environment", "key", "value", "description"]

    # Search configuration
    search_columns = ["environment", "key", "value", "description"]

    # Labeling for better UI
    label_columns = {
        "environment": "Environment",
        "key": "Setting Key",
        "value": "Setting Value",
        "description": "Description",
        "created_at": "Created On",
        "updated_at": "Last Updated On",
    }

    # Field ordering
    add_fieldsets = [
        ("Setting Details", {"fields": ["environment", "key", "value", "description"]})
    ]
    edit_fieldsets = add_fieldsets

    # ✅ Thêm phương thức kiểm tra `datamodel`
    def check_datamodel(self):
        if self.datamodel is None:
            raise ValueError("datamodel is not initialized properly in AppSettingView")

    # ✅ Kiểm tra và sửa lỗi nếu `datamodel` chưa được khởi tạo
    def get_value(self, attribute_name):
        self.check_datamodel()  # Kiểm tra trước khi truy xuất thuộc tính
        return getattr(self, attribute_name, None)  # ✅ Tránh lỗi `super()

    # You can add validators or custom widgets here if needed
    # For example, for the 'value' field if it's JSON:
    # from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget
    # edit_form_extra_fields = {'value': StringField('Value (JSON)', widget=BS3TextAreaFieldWidget())}
    # add_form_extra_fields = edit_form_extra_fields

    # Optional: Add actions
    # from flask_appbuilder.actions import action
    # @action("my_action", "My Action", "Do something?", "fa-rocket")
    # def my_action(self, items):
    #     # self.update_redirect()
    #     # return redirect(self.get_redirect())
    #     pass


# You can add more views here for other models or custom pages
