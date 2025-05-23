from __future__ import annotations

import pendulum
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple

from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationError

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator
from airflow.providers.email.operators.email import EmailOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from airflow.utils.log.logging_mixin import LoggingMixin # For logging within functions

# --- Pydantic Task Model (aligns with get_tasks_for_dag function output) ---
class TaskDefinitionModel(BaseModel):
    task_id: int
    parent_task_id: Optional[int] = None
    task_order: int = 0
    task_type: str
    task_name: str
    run_time: Optional[int] = None
    config_key_name: Optional[str] = None
    process_num: Optional[int] = 1
    frequency: Optional[str] = None
    day_of_week: Optional[int] = None
    day_of_month: Optional[int] = None
    script: Optional[str] = None
    connection_string: Optional[str] = None
    output_name: Optional[str] = None # Raw string from DB
    src_folder_name: Optional[str] = None
    src_file_name: Optional[str] = None
    src_file_type: Optional[str] = None
    dst_folder_name: Optional[str] = None
    dst_file_name: Optional[str] = None
    dst_file_type: Optional[str] = None
    is_header: Optional[bool] = False
    is_notification: Optional[bool] = False
    is_attachment: Optional[bool] = False
    email: Optional[str] = None # Raw string from DB
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    task_time_out: Optional[int] = 0
    retry_number: Optional[int] = 0
    sub_task_max_retry: Optional[int] = 3
    is_sub_task: Optional[bool] = False
    is_frequency_task: Optional[bool] = False
    is_notify_fail: Optional[bool] = False
    is_notify_sucess: Optional[bool] = False

    # Parsed fields (for convenience after validation)
    parsed_email_list: List[EmailStr] = Field(default_factory=list, exclude=True)
    parsed_output_name_list: List[str] = Field(default_factory=list, exclude=True)

    @field_validator('email', mode='before')
    def _parse_email_str(cls, v: Optional[str]) -> str: # Keep original for model, parse into separate field
        return v or ""

    @field_validator('output_name', mode='before')
    def _parse_output_name_str(cls, v: Optional[str]) -> str: # Keep original for model
        return v or ""

    def model_post_init(self, __context: Any) -> None:
        # Post-initialization parsing
        if self.email:
            try:
                self.parsed_email_list = [EmailStr(e.strip()) for e in self.email.replace(';', ',').split(',') if e.strip()]
            except ValidationError:
                # Handle or log invalid email formats if necessary
                self.parsed_email_list = [] 
        if self.output_name:
            self.parsed_output_name_list = [o.strip() for o in self.output_name.replace(';', ',').split(',') if o.strip()]

    class Config:
        frozen = False
        extra = 'ignore'
        from_attributes = True # Allows creating from ORM objects or dicts with matching names

# --- Function to fetch tasks using the PostgreSQL function ---
def fetch_task_definitions_from_db(
    postgres_conn_id: str, 
    current_run_time: int, # e.g., 1605 for 4:05 PM
    task_id_filter: int = -1 # -1 for all relevant tasks
) -> List[TaskDefinitionModel]:
    log = LoggingMixin().log
    pg_hook = PostgresHook(postgres_conn_id=postgres_conn_id)
    sql_call = f"SELECT * FROM airflow.get_tasks_for_dag(p_run_time => %s, p_task_id => %s);"
    
    log.info(f"Executing SQL to fetch tasks: {sql_call} with params ({current_run_time}, {task_id_filter})")
    
    try:
        # get_records returns list of tuples. We need to map them to dicts.
        # The column names are defined by the RETURN TABLE of get_tasks_for_dag
        column_names = [
            'task_id', 'parent_task_id', 'task_order', 'task_type', 'task_name',
            'run_time', 'config_key_name', 'process_num', 'frequency', 'day_of_week',
            'day_of_month', 'script', 'connection_string', 'output_name',
            'src_folder_name', 'src_file_name', 'src_file_type', 'dst_folder_name',
            'dst_file_name', 'dst_file_type', 'is_header', 'is_notification',
            'is_attachment', 'email', 'start_date', 'end_date', 'task_time_out',
            'retry_number', 'sub_task_max_retry', 'is_sub_task', 'is_frequency_task',
            'is_notify_fail', 'is_notify_sucess'
        ]
        
        records: List[Tuple] = pg_hook.get_records(sql=sql_call, parameters=(current_run_time, task_id_filter))
        
        task_defs = []
        if records:
            log.info(f"Fetched {len(records)} raw task records from database.")
            for record_tuple in records:
                record_dict = dict(zip(column_names, record_tuple))
                try:
                    task_model = TaskDefinitionModel(**record_dict)
                    task_defs.append(task_model)
                except ValidationError as e:
                    log.error(f"Pydantic validation error for record {record_dict.get('task_id', 'N/A')}: {e}")
                except Exception as e_gen:
                    log.error(f"General error parsing record {record_dict.get('task_id', 'N/A')}: {e_gen}")
        else:
            log.info("No task records found for the given criteria.")
        return task_defs
    except Exception as e:
        log.error(f"Error fetching or parsing task definitions from DB: {e}")
        return []

# --- DAG Definition ---
# Use the Airflow default connection for PostgreSQL unless specified otherwise
AIRFLOW_DB_CONN_ID = "airflow_db" 

# Determine the current run time for fetching tasks.
# This needs to be dynamic based on the DAG's schedule or manual trigger time.
# For a DAG scheduled every 5 minutes, you might calculate the "slot".
# Example: if current time is 16:07, run_time_slot could be 1605.
# This logic depends on how your `run_time` field in the DB is intended to be used.
# For simplicity, we'll use a fixed value or pass it via config.
# A more robust way is to use {{ data_interval_start }} or similar macros.
current_dag_run_time_slot = int(pendulum.now("UTC").strftime("%H%M")) # Example: 1607 for 4:07 PM UTC

with DAG(
    dag_id="dynamic_dag_from_postgres_function",
    start_date=days_ago(1),
    catchup=False,
    schedule="*/5 * * * *", # Example: Run every 5 minutes
    tags=['dynamic', 'postgres-function', 'database-driven'],
    render_template_as_native_obj=True,
    doc_md="""
    ### Dynamic DAG from PostgreSQL Function
    This DAG fetches task definitions from the `custom_task_definitions` table
    by calling the `airflow.get_tasks_for_dag` PostgreSQL function.
    It then dynamically creates Airflow tasks based on these definitions.
    The `AIRFLOW_DB_CONN_ID` should point to your Airflow metadata database (PostgreSQL).
    The `current_dag_run_time_slot` is used to filter tasks from the DB function.
    """
) as dag:
    start_pipeline = EmptyOperator(task_id="start_pipeline")
    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # Fetch and parse task definitions using the Python function
    # This call happens at DAG parsing time.
    # For production, if DB calls are slow or numerous, consider strategies
    # like using a PythonOperator to fetch and then TaskFlow API or XComs.
    
    # Calculate run_time based on DAG schedule (e.g., floor to nearest 5 min)
    # This is a placeholder; actual calculation might be more complex based on your needs
    # For a */5 * * * * schedule, data_interval_start will be on a 5-min boundary
    # run_time_for_query = "{{ data_interval_start.strftime('%H%M') }}" # This would be a string
    # For now, let's assume a Python callable handles this or it's passed via config.
    # We'll use a fixed value for demonstration in this simplified parsing-time call.
    # A better way for dynamic run_time_for_query:
    # Use a PythonOperator to calculate it and push to XCom, then another to generate tasks.
    # Or, if the number of tasks isn't excessively large, this parsing-time call might be acceptable.
    
    # Get the current hour and minute, rounded to the nearest 5-minute interval for the query
    now = pendulum.now("UTC")
    minute_rounded = (now.minute // 5) * 5
    query_run_time = int(f"{now.hour:02d}{minute_rounded:02d}")

    log = LoggingMixin().log # Get a logger instance
    log.info(f"DAG parsing: Using query_run_time = {query_run_time} to fetch tasks.")

    task_objects = fetch_task_definitions_from_db(
        postgres_conn_id=AIRFLOW_DB_CONN_ID,
        current_run_time=query_run_time # Pass the calculated run time
    )
    
    log.info(f"DAG parsing: Fetched {len(task_objects)} task objects.")

    airflow_tasks: Dict[int, Any] = {} # Stores Airflow operator instances, keyed by original task_id

    if not task_objects:
        log.warning("No task objects fetched. DAG will have only start and end nodes.")
        start_pipeline >> end_pipeline
    else:
        # Create Airflow Operators from TaskDefinitionModel objects
        for task_def in task_objects:
            task_airflow_id = f"{task_def.task_name.replace(' ', '_').replace('.', '_')}_task_{task_def.task_id}"
            
            operator_args = {
                "task_id": task_airflow_id,
                "dag": dag,
                "retries": task_def.retry_number or 0,
            }
            if task_def.task_time_out and task_def.task_time_out > 0:
                operator_args["execution_timeout"] = timedelta(seconds=task_def.task_time_out)

            current_op = None
            script_content = task_def.script if task_def.script else ""

            if task_def.task_type == "BASH":
                current_op = BashOperator(
                    **operator_args,
                    bash_command=script_content or "echo 'No script for BASH task'"
                )
            elif task_def.task_type == "PYTHON":
                def _execute_python_callable(script_to_execute, **kwargs):
                    log_py = LoggingMixin().log
                    log_py.info(f"Executing Python task via callable: {kwargs['ti'].task_id}")
                    log_py.info(f"Script content/path: {script_to_execute}")
                    try:
                        # If script_to_execute is a path to a .py file:
                        # import importlib.util
                        # spec = importlib.util.spec_from_file_location("custom_module", script_to_execute)
                        # custom_module = importlib.util.module_from_spec(spec)
                        # spec.loader.exec_module(custom_module)
                        # custom_module.run() # Assuming a 'run' function in the script
                        # Or, if script_to_execute is actual Python code:
                        exec(script_to_execute, {"log": log_py, "kwargs": kwargs}) # Provide log and context
                        log_py.info(f"Python task {kwargs['ti'].task_id} completed.")
                    except Exception as e_py_exec:
                        log_py.error(f"Error in Python callable for {kwargs['ti'].task_id}: {e_py_exec}")
                        raise

                current_op = PythonOperator(
                    **operator_args,
                    python_callable=_execute_python_callable,
                    op_kwargs={"script_to_execute": script_content}
                )
            elif task_def.task_type == "SQL" and task_def.connection_string:
                current_op = PostgresOperator( # Assuming Postgres, change if different DB
                    **operator_args,
                    postgres_conn_id=task_def.connection_string,
                    sql=script_content # Assumes script is a single SQL command or list of commands
                )
            elif task_def.task_type in ("SFTP_PUT", "SFTP_GET") and task_def.connection_string:
                sftp_op_type = "put" if task_def.task_type == "SFTP_PUT" else "get"
                local_path = f"{task_def.src_folder_name or '.'}/{task_def.src_file_name or 'default_file'}"
                remote_path = f"{task_def.dst_folder_name or '/remote'}/{task_def.dst_file_name or task_def.src_file_name or 'default_file'}"
                if sftp_op_type == "get": # Swap for get
                    local_path, remote_path = remote_path, local_path

                current_op = SFTPOperator(
                    **operator_args,
                    sftp_conn_id=task_def.connection_string,
                    local_filepath=local_path,
                    remote_filepath=remote_path,
                    operation=sftp_op_type,
                    create_intermediate_dirs=True
                )
            elif task_def.task_type == "EMAIL" and task_def.connection_string and task_def.parsed_email_list:
                email_subject = f"Airflow Task Notification: {task_def.task_name} (ID: {task_def.task_id})"
                email_content = script_content or f"Task {task_def.task_name} (ID: {task_def.task_id}) status update."
                
                # Handle trigger rules based on notification flags
                if task_def.is_notify_fail and not task_def.is_notify_sucess:
                     operator_args["trigger_rule"] = "one_failed"
                elif task_def.is_notify_sucess and not task_def.is_notify_fail:
                     operator_args["trigger_rule"] = "all_success" # Default, but explicit
                elif task_def.is_notify_fail and task_def.is_notify_sucess:
                     operator_args["trigger_rule"] = "all_done"


                current_op = EmailOperator(
                    **operator_args,
                    to=task_def.parsed_email_list,
                    subject=email_subject,
                    html_content=email_content,
                    conn_id=task_def.connection_string,
                    # files=task_def.parsed_output_name_list if task_def.is_attachment else None # Requires files to be accessible
                )
            else:
                log.warning(f"Unhandled or misconfigured task_type '{task_def.task_type}' for task_id {task_def.task_id}. Creating EmptyOperator.")
                current_op = EmptyOperator(**operator_args)

            if current_op:
                airflow_tasks[task_def.task_id] = current_op
            else:
                log.error(f"Failed to create operator for task_id {task_def.task_id}")


        # Set up dependencies
        for task_def in task_objects:
            current_airflow_task = airflow_tasks.get(task_def.task_id)
            if not current_airflow_task:
                log.warning(f"Could not find created Airflow task for DB task_id {task_def.task_id} during dependency setup.")
                continue

            if task_def.parent_task_id and task_def.parent_task_id in airflow_tasks:
                parent_airflow_task = airflow_tasks[task_def.parent_task_id]
                parent_airflow_task >> current_airflow_task
            else:
                start_pipeline >> current_airflow_task

            is_leaf_node = True
            for other_task_def in task_objects:
                if other_task_def.parent_task_id == task_def.task_id:
                    is_leaf_node = False
                    break
            if is_leaf_node:
                current_airflow_task >> end_pipeline
        
        if not start_pipeline.downstream_task_ids and not end_pipeline.upstream_task_ids and airflow_tasks:
             log.error("Critical error in dependency setup: No tasks linked to start_pipeline, but tasks exist.")
             # Fallback: link all tasks without upstreams (other than start_pipeline) to start_pipeline
             # And all tasks without downstreams (other than end_pipeline) to end_pipeline
             # This indicates a flaw in the parent_task_id logic from the DB or its interpretation.
             # For now, this situation should be reviewed if it occurs.
        elif not start_pipeline.downstream_task_ids and airflow_tasks:
             log.warning("No tasks were connected to start_pipeline. Check parent_task_id logic.")
        
        if not end_pipeline.upstream_task_ids and airflow_tasks:
             log.warning("No tasks were connected to end_pipeline. Check leaf node detection.")


# Example of how you might call the PG function from psql or a DB tool:
# SELECT * FROM airflow.get_tasks_for_dag(p_run_time := 1605, p_task_id := -1);