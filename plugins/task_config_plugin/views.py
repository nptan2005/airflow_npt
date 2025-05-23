from flask_appbuilder import ModelView
from flask_appbuilder.models.sqla.interface import SQLAInterface

# from wtforms.fields import StringField, TextAreaField # For custom field rendering if needed
from wtforms.fields import TextAreaField

# from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget, Select2Widget # Example widgets
from flask_appbuilder.fieldwidgets import Select2Widget
from task_config_plugin.models import TaskDefinition


class TaskDefinitionView(ModelView):
    datamodel = SQLAInterface(TaskDefinition)

    list_title = "Task Definitions"
    show_title = "Task Definition Details"
    add_title = "Add New Task Definition"
    edit_title = "Edit Task Definition"

    # Columns to display in the list view
    list_columns = [
        "task_name",
        "task_type",
        "parent_task_id",
        "task_order",
        "active",
        "connection_string",
        "frequency",
        "updated_at",
    ]

    # Columns to display in the show/details view (can be more comprehensive)
    show_fieldsets = [
        (
            "Summary",
            {
                "fields": [
                    "task_name",
                    "task_type",
                    "active",
                    "parent_task_id",
                    "task_order",
                ]
            },
        ),
        (
            "Execution Details",
            {"fields": ["connection_string", "script", "config_key_name"]},
        ),
        (
            "Scheduling",
            {
                "fields": [
                    "run_time",
                    "frequency",
                    "day_of_week",
                    "day_of_month",
                    "start_date",
                    "end_date",
                ]
            },
        ),
        (
            "Timing & Retries",
            {"fields": ["task_time_out", "retry_number", "sub_task_max_retry"]},
        ),
        (
            "File/Data Handling",
            {
                "fields": [
                    "output_name",
                    "src_folder_name",
                    "src_file_name",
                    "src_file_type",
                    "dst_folder_name",
                    "dst_file_name",
                    "dst_file_type",
                ]
            },
        ),
        (
            "Flags & Notifications",
            {"fields": ["is_header", "is_notification", "is_attachment", "email"]},
        ),
        ("Process Control", {"fields": ["process_num"]}),
        (
            "Audit Info",
            {
                "fields": [
                    "request_department",
                    "request_user",
                    "request_date",
                    "process_user",
                    "process_date",
                    "created_at",
                    "updated_at",
                ]
            },
        ),
    ]

    # Columns for add/edit forms
    # Grouping them into fieldsets for better organization
    add_fieldsets = [
        (
            "Basic Info",
            {
                "fields": [
                    "task_name",
                    "task_type",
                    "active",
                    "parent_task_id",
                    "task_order",
                ]
            },
        ),
        (
            "Execution & Connection",
            {
                "fields": ["connection_string", "script", "config_key_name"],
                "description": "Enter script content or path. Specify Airflow connection ID.",
            },
        ),
        (
            "Scheduling Parameters",
            {
                "fields": [
                    "run_time",
                    "frequency",
                    "day_of_week",
                    "day_of_month",
                    "start_date",
                    "end_date",
                ]
            },
        ),
        (
            "Advanced Timing & Retries",
            {"fields": ["task_time_out", "retry_number", "sub_task_max_retry"]},
        ),
        (
            "File Transfer / Data Source & Destination",
            {
                "fields": [
                    "output_name",
                    "src_folder_name",
                    "src_file_name",
                    "src_file_type",
                    "dst_folder_name",
                    "dst_file_name",
                    "dst_file_type",
                ]
            },
        ),
        (
            "Notifications & Flags",
            {"fields": ["is_header", "is_notification", "is_attachment", "email"]},
        ),
        (
            "Process & Audit (Optional)",
            {
                "fields": [
                    "process_num",
                    "request_department",
                    "request_user",
                    "request_date",
                ],
                "expanded": False,  # Collapsed by default
            },
        ),
    ]
    # Edit form can reuse add_fieldsets or have its own
    edit_fieldsets = add_fieldsets

    # Searchable columns
    search_columns = [
        "task_name",
        "task_type",
        "connection_string",
        "script",
        "frequency",
        "email",
    ]

    # Order list view by task_name by default
    order_columns = ["task_name"]

    # Custom labels for UI clarity
    label_columns = {
        "task_name": "Task Name",
        "task_type": "Task Type (e.g., BASH, PYTHON, SQL)",
        "parent_task_id": "Parent Task ID (for dependencies)",
        "task_order": "Order (for parallel tasks under same parent)",
        "active": "Is Active",
        "connection_string": "Airflow Connection ID",
        "script": "Script / Command / Query",
        "config_key_name": "Config Key (if any)",
        "run_time": "Run Time (e.g., 0800 or duration)",
        "frequency": "Frequency (e.g., DAILY, HOURLY, CRON)",
        "day_of_week": "Day of Week (1-7)",
        "day_of_month": "Day of Month (1-31)",
        "task_time_out": "Timeout (seconds)",
        "retry_number": "Retries",
        "sub_task_max_retry": "Sub-Task Max Retries",
        "output_name": "Output Name(s) (CSV or JSON)",
        "src_folder_name": "Source Folder",
        "src_file_name": "Source File",
        "src_file_type": "Source File Type",
        "dst_folder_name": "Destination Folder",
        "dst_file_name": "Destination File",
        "dst_file_type": "Destination File Type",
        "is_header": "Is Grouping Header",
        "is_notification": "Enable Notification",
        "is_attachment": "Include Attachment",
        "email": "Notification Email(s) (CSV or JSON)",
        "process_num": "Parallel Process Limit",
        "request_department": "Requesting Dept.",
        "request_user": "Requested By",
        "request_date": "Request Date",
        "process_user": "Processed By",
        "process_date": "Processed Date",
        "created_at": "Created At",
        "updated_at": "Updated At",
    }

    # Use TextArea for script and email fields for better multi-line editing
    form_overrides = {
        "script": TextAreaField,
        "email": TextAreaField,
        "output_name": TextAreaField,
        "config_key_name": TextAreaField,
    }
    form_widget_args = {
        "script": {
            "rows": 10,
            "placeholder": "Enter your bash command, SQL query, Python script path, or Python code here...",
        },
        "email": {
            "rows": 3,
            "placeholder": "john.doe@example.com, jane.doe@example.com",
        },
        "output_name": {
            "rows": 2,
            "placeholder": "output_file.csv, another_result.json",
        },
        "config_key_name": {
            "rows": 2,
            "placeholder": "e.g., MY_API_SETTINGS_KEY (references another config)",
        },
        "parent_task_id": {
            "widget": Select2Widget(),  # Makes parent_task_id a searchable dropdown if you have many tasks
            "query_func": lambda: TaskDefinitionView.datamodel.session.query(
                TaskDefinition.id, TaskDefinition.task_name
            ).all(),
            # This query_func might need adjustment based on how you want to display parent tasks.
            # For a simple dropdown of IDs, it's fine. For names, you'd need a custom field or converter.
        },
    }
    # For parent_task_id, it might be better to use a related_view or a custom field
    # if you want to select by task_name instead of ID directly in the form.
    # This example keeps it simple with ID.

    # You can add custom validators here
    # def pre_add(self, item):
    #     # item.script = "Validated: " + item.script
    #     pass

    # def pre_update(self, item):
    #     # item.updated_at = datetime.utcnow() # Already handled by onupdate
    #     pass
