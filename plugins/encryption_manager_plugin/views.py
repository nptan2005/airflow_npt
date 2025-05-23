from flask import flash, request
from flask_appbuilder import ModelView, BaseView, expose, SimpleFormView
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.fieldwidgets import BS3TextAreaFieldWidget # Correct import
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired
from .models import EncryptedDataRef
from airflow.utils.session import provide_session # For database operations in custom views

# Import your encryption module
# This assumes 'modules' is in PYTHONPATH or the plugin is structured to include it.
# For Airflow plugins, it's better if 'multiAlgoCoder' is a proper package
# installable in the Airflow environment, or its path is added to sys.path.
# For now, we'll try a relative import path assuming a certain structure or PYTHONPATH setup.
# If 'modules' is at the root of the Airflow project:
import sys
import os

# Add 'modules' directory to sys.path if it's not already there.
# This is a common way to make modules accessible in Airflow plugins,
# but packaging 'multiAlgoCoder' as a library is cleaner for production.
# Assuming AIRFLOW_HOME is the project root or 'modules' is relative to DAGs/plugins.
# This path adjustment might need to be more robust depending on your Airflow deployment.
try:
    # Attempt to find the 'modules' directory relative to the plugin or a known base path
    # This is a common pattern but might need adjustment based on your project structure
    plugin_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(plugin_dir, '..', '..')) # Adjust if modules is elsewhere
    modules_path = os.path.join(project_root, 'modules')
    if modules_path not in sys.path:
        sys.path.insert(0, modules_path)
    from multiAlgoCoder import generateKey # Now try importing
except ImportError as e:
    # Fallback if the above path logic doesn't work, try a simpler import
    # This relies on PYTHONPATH being correctly set in the Airflow environment
    try:
        from multiAlgoCoder import generateKey
    except ImportError:
        generateKey = None # Set to None if import fails, to be handled in methods
        flash(f"Critical: Could not import 'multiAlgoCoder.generateKey'. Encryption will fail. Error: {e}", "error")


# Form for encrypting new data
class EncryptDataForm(SimpleFormView.form):
    tab_name = StringField('Tab Name / Identifier', validators=[DataRequired()],
                           description="A unique name to identify this encrypted data (e.g., 'DB_PASSWORD_X', 'API_SECRET_Y').")
    plain_text_data = TextAreaField('Data to Encrypt', validators=[DataRequired()],
                                 widget=BS3TextAreaFieldWidget(), # Now correctly referenced
                                 description="The sensitive data you want to encrypt.")
    description = TextAreaField('Description (Optional)',
                                description="A brief note about what this encrypted data is for.")
    submit = SubmitField("Encrypt and Save Reference")


# Custom View for the encryption form and processing
class EncryptDataView(BaseView):
    route_base = "/encryption_manager/encrypt"
    default_view = "encrypt_form"

    @expose("/form/", methods=["GET", "POST"])
    @provide_session
    def encrypt_form(self, session=None):
        if not generateKey:
            flash("Encryption module (generateKey) is not available. Cannot perform encryption.", "error")
            return self.render_template("error_page.html", error_message="Encryption module missing.")

        form = EncryptDataForm(request.form)
        if request.method == 'POST' and form.validate():
            tab_name_input = form.tab_name.data
            plain_text = form.plain_text_data.data
            desc = form.description.data

            try:
                # Check if tab_name already exists
                existing_ref = session.query(EncryptedDataRef).filter_by(tab_name=tab_name_input).first()
                if existing_ref:
                    flash(f"Error: Tab Name '{tab_name_input}' already exists. Please use a unique name.", "error")
                    return self.render_template("encrypt_form.html", form=form, title="Encrypt New Data")

                # Perform encryption using your module
                # Ensure that the 'bin' directory and necessary key files for generateKey are accessible
                # by the Airflow webserver/worker environment.
                encoded_tab_ref = generateKey.encode_str(value=plain_text, tab=tab_name_input)

                # Save the reference to the database
                new_ref = EncryptedDataRef(
                    tab_name=tab_name_input,
                    encoded_tab_reference=encoded_tab_ref,
                    description=desc
                )
                session.add(new_ref)
                session.commit()
                flash(f"Data encrypted successfully for Tab Name: '{tab_name_input}'. Reference stored.", "success")
                flash(f"Encoded Reference (keep this safe if needed, but it's stored): {encoded_tab_ref}", "info")
                # Optionally, redirect to the list view or clear the form
                # return redirect(url_for('EncryptedDataRefView.list'))
            except Exception as e:
                session.rollback()
                flash(f"Encryption or database error: {e}", "error")
                # Log the full error for debugging
                self.appbuilder.sm.get_current_user().logger.error(f"Encryption error: {e}", exc_info=True)


        return self.render_template("encrypt_form.html", form=form, title="Encrypt New Data")
        # This requires a template file: plugins/encryption_manager_plugin/templates/encrypt_form.html


# ModelView for listing and viewing details of stored encrypted references
class EncryptedDataRefView(ModelView):
    datamodel = SQLAInterface(EncryptedDataRef)
    
    list_title = "Stored Encrypted Data References"
    list_columns = ['tab_name', 'description', 'encoded_tab_reference', 'created_at', 'updated_at']
    show_columns = ['tab_name', 'description', 'encoded_tab_reference', 'created_at', 'updated_at']
    
    # Make 'encoded_tab_reference' read-only in edit view if direct editing is allowed
    # edit_columns = ['tab_name', 'description'] # If ref should not be editable
    # For now, allow editing description, but not the core fields easily.
    # If you allow editing tab_name, the underlying encrypted files won't match.
    edit_form_rules = (
        'tab_name', # Should ideally be read-only after creation or handled carefully
        'description',
        # 'encoded_tab_reference' # Should be read-only
    )
    # Add is more complex as it involves encryption, handled by EncryptDataView

    search_columns = ['tab_name', 'description', 'encoded_tab_reference']
    
    label_columns = {
        'tab_name': 'Tab Name / Identifier',
        'encoded_tab_reference': 'Encoded Reference (from encode_str)',
        'description': 'Description',
        'created_at': 'Created On',
        'updated_at': 'Last Updated On'
    }
    
    # Disabling add/delete directly on this ModelView as 'add' is custom
    # and 'delete' needs to consider cleanup of associated encrypted files (advanced).
    # For now, delete will just remove the DB record.
    # can_add = False
    # can_delete = True # Set to False if file cleanup is a concern and not implemented

    # If you want a button to go to the custom encryption form from this list view
    # you can add it via a custom template or an action.