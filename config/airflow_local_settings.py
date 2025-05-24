import os

BASE_LOG_FOLDER = os.environ.get("LOG_PATH", "/opt/airflow/logs")
PROCESSOR_LOG_FOLDER = os.path.join(BASE_LOG_FOLDER, "scheduler")

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(levelname)s] %(name)s - %(message)s',
        },
        'task': {
            'format': '[%(asctime)s] [%(levelname)s] %(filename)s:%(lineno)d - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'stream': 'ext://sys.stdout',
        },
        'task_file_handler': {
            'class': 'airflow.utils.log.file_task_handler.FileTaskHandler',
            'formatter': 'task',
            'base_log_folder': BASE_LOG_FOLDER,
            'filename_template': '{{ ti.dag_id }}/{{ ti.task_id }}/{{ ts }}/{{ try_number }}.log',
        },
        'processor': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'default',
            'filename': os.path.join(PROCESSOR_LOG_FOLDER, 'dag_processor.log'),
            'when': 'midnight',
            'backupCount': 7,
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        'airflow': {
            'handlers': ['console', 'processor'],
            'level': os.getenv("AIRFLOW__LOGGING__LOGGING_LEVEL", "INFO"),
            'propagate': False,
        },
        'airflow.task': {
            'handlers': ['task_file_handler', 'console'],
            'level': os.getenv("AIRFLOW__LOGGING__LOGGING_LEVEL", "INFO"),
            'propagate': False,
        },
        'airflow.processor': {
            'handlers': ['processor'],
            'level': os.getenv("AIRFLOW__LOGGING__LOGGING_LEVEL", "INFO"),
            'propagate': False,
        },
        'airflow.task_runner': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console'],
        'level': os.getenv("AIRFLOW__LOGGING__LOGGING_LEVEL", "INFO"),
    }
}