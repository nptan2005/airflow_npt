import json  # For handling JSON data in forms
from flask_appbuilder import ModelView, CompactCRUDMixin
from flask_appbuilder.models.sqla.interface import SQLAInterface

# from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget # For JSON text areas
# from wtforms import TextAreaField, BooleanField
from wtforms import TextAreaField

# from wtforms.validators import Optional as WTFormsOptional # Renamed to avoid conflict
from data_template_config_plugin.models import (
    DBImportTemplate,
    DBExportTemplate,
    DBExportSheetConfig,
)


# Helper to handle JSON conversion for form fields
class JSONTextAreaField(TextAreaField):
    def _value(self):
        if self.data:
            try:
                return json.dumps(self.data, indent=2)
            except TypeError:  # data is not serializable
                return ""
        return ""

    def process_formdata(self, valuelist):
        if valuelist and valuelist[0]:
            try:
                self.data = json.loads(valuelist[0])
            except json.JSONDecodeError:
                self.data = None  # Or raise ValidationError
                raise ValueError("Invalid JSON data in field.")
        else:
            self.data = None


class DBImportTemplateView(ModelView):
    datamodel = SQLAInterface(DBImportTemplate)

    list_title = "Import Templates"
    show_title = "Import Template Details"
    add_title = "Add Import Template"
    edit_title = "Edit Import Template"

    list_columns = [
        "template_name",
        "file_extension",
        "table_name",
        "procedure_name",
        "sftp_conn",
        "updated_at",
    ]
    show_fieldsets = [
        (
            "Basic Info",
            {"fields": ["template_name", "description", "file_extension", "separate"]},
        ),
        ("File & SFTP", {"fields": ["sftp_conn", "sftp_move"]}),
        (
            "Parsing Rules",
            {
                "fields": [
                    "start_row",
                    "end_row",
                    "start_col",
                    "end_col",
                    "is_read_to_empty_row",
                ]
            },
        ),
        (
            "Database Target",
            {
                "fields": [
                    "table_name",
                    "is_truncate_tmp_table",
                    "procedure_name",
                    "external_process",
                ]
            },
        ),
        ("Header & Mapping (JSON)", {"fields": ["header_json", "column_mapping_json"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "expanded": False}),
    ]

    add_columns = [
        "template_name",
        "description",
        "file_extension",
        "separate",
        "sftp_conn",
        "sftp_move",
        "start_row",
        "end_row",
        "start_col",
        "end_col",
        "is_read_to_empty_row",
        "table_name",
        "is_truncate_tmp_table",
        "procedure_name",
        "external_process",
        "header_json",
        "column_mapping_json",
    ]
    edit_columns = add_columns

    form_overrides = {
        "header_json": JSONTextAreaField,
        "column_mapping_json": JSONTextAreaField,
        # WTForms BooleanField handles 'true'/'false' strings by default if not strict.
        # If your Pydantic bool parsing was more complex (e.g. '1'/'0'), you might need custom fields.
    }
    form_widget_args = {
        "header_json": {
            "rows": 5,
            "placeholder": 'Enter JSON array of strings, e.g., ["ColA", "ColB"]',
        },
        "column_mapping_json": {
            "rows": 10,
            "placeholder": 'Enter JSON object, e.g., {"SourceColA": "TargetColA"}',
        },
        "sftp_move": {"label_text": "SFTP Move After Transfer"},
        "is_read_to_empty_row": {"label_text": "Read To Empty Row"},
        "is_truncate_tmp_table": {"label_text": "Truncate Temp Table"},
    }

    label_columns = {
        "template_name": "Template Name",
        "header_json": "Header (JSON Array)",
        "column_mapping_json": "Column Mapping (JSON Object)",
        # Add other labels as needed
    }


# Inline view for DBExportSheetConfig, used within DBExportTemplateView
class DBExportSheetConfigViewInline(CompactCRUDMixin, ModelView):  # Or just ModelView
    datamodel = SQLAInterface(DBExportSheetConfig)
    # list_title = "Sheet Configurations" # Not shown in inline
    # can_add = True
    # can_edit = True
    # can_delete = True

    edit_columns = [
        "sheet_name_key",
        "sheet_display_name",
        "is_header",
        "sheet_title_name",
        "is_format",
        "column_mapping_json",
    ]
    add_columns = edit_columns

    form_overrides = {
        "column_mapping_json": JSONTextAreaField,
    }
    form_widget_args = {
        "column_mapping_json": {
            "rows": 5,
            "placeholder": 'JSON: {"SourceCol": "ExcelHeader"}',
        },
    }
    label_columns = {
        "sheet_name_key": "Sheet Key (Internal)",
        "sheet_display_name": "Sheet Name (Excel Tab)",
        "is_header": "Include Header Row",
        "sheet_title_name": "Sheet Title (Optional)",
        "is_format": "Apply Formatting",
        "column_mapping_json": "Column Mapping (JSON)",
    }


class DBExportTemplateView(ModelView):
    datamodel = SQLAInterface(DBExportTemplate)

    list_title = "Export Templates"
    show_title = "Export Template Details"
    add_title = "Add Export Template"
    edit_title = "Edit Export Template"

    list_columns = [
        "template_name",
        "file_extension",
        "sftp_conn",
        "sftp_move",
        "updated_at",
    ]

    add_columns = [
        "template_name",
        "description",
        "file_extension",
        "separate",
        "sftp_conn",
        "sftp_move",
    ]
    edit_columns = add_columns

    show_fieldsets = [
        (
            "Basic Info",
            {"fields": ["template_name", "description", "file_extension", "separate"]},
        ),
        ("SFTP", {"fields": ["sftp_conn", "sftp_move"]}),
        ("Timestamps", {"fields": ["created_at", "updated_at"], "expanded": False}),
    ]

    # Inline view for managing sheets associated with an export template
    related_views = [DBExportSheetConfigViewInline]

    # When showing an export template, also show its sheets
    show_template = (
        "appbuilder/general/model/show_cascade.html"  # Default, but explicit
    )
    edit_template = "appbuilder/general/model/edit_cascade.html"

    label_columns = {
        "template_name": "Template Name",
        "sftp_move": "SFTP Move After Transfer",
    }
