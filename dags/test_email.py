from airflow.providers.smtp.operators.smtp import EmailOperator

with DAG("email_dag", start_date=datetime(2025, 4, 16)) as dag:
    email_task = EmailOperator(
        task_id="send_email",
        smtp_conn_id="smtp_default",
        to="receiver@domain.com",
        subject="Test Email",
        html_content="<h3>Sample Email</h3>"
    )