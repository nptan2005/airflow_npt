from airflow import DAG
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd

def export_to_excel():
    try:
        # Kết nối tới PostgreSQL bằng PostgresHook
        hook = PostgresHook(postgres_conn_id='mms_slave_db_conn')
        conn = hook.get_conn()
        cursor = conn.cursor()

        # Query dữ liệu từ PostgreSQL
    #     query = """
    #             SELECT a.id, a.txn_id
    #                 , TO_CHAR(TO_TIMESTAMP(a.created_unix_time), 'DD-MM-YYYY HH24:MI:SS') AS created_time
    #                 , TO_CHAR(TO_TIMESTAMP(a.updated_unix_time), 'DD-MM-YYYY HH24:MI:SS') AS updated_time
    #                 , a.mid, a.tid, a.serial_no, a.card_no
    #                 , a.batch_no, a.invoice_no, a.card_origin, a.bank_code, a.card_type, a.is_credit
    #                 , a.mcc_international
    #                 , a.pos_entry_mode, a.routing_bank_code
    #                 , a.transaction_type, a.request_amount, a.tip
    #                 , a.response_code, a.is_settle, a.is_void, a.is_refund, a.is_clear_batch

    #                 , a.system_trace_no
    #                 , a.retrieval_ref_no, a.auth_id_response

    #                 , a.msp_code, a.msp_price, a.fee_percentage, a.longitude, a.latitude
    #                 , a.primary_account, a.primary_account_name
    #                 --, a.*
    #                 , TO_TIMESTAMP(CAST(a.original_transaction_date AS INT))::DATE AS orig_txn_date
    #                 , TO_CHAR(TO_TIMESTAMP(a.settle_unix_time), 'DD-MM-YYYY HH24:MI:SS') AS settle_time
    #                 , TO_CHAR(TO_TIMESTAMP(a.void_unix_time), 'DD-MM-YYYY HH24:MI:SS') AS void_time
    #                 , TO_CHAR(TO_TIMESTAMP(a.reversal_unix_time), 'DD-MM-YYYY HH24:MI:SS') AS reversal_time
    #                 FROM public.transaction_model a;
    # """  
    
        query = """
            SELECT datname AS database_name
                FROM pg_database
                WHERE datistemplate = false;
                with maping_user as (
                        select name, rs.id as res_user_id, rp as res_partner_id from res_partner rp left join res_users rs on rs.partner_id = rp.id
                    ), log_note as (
                        select res_id as partner_id, json_agg(body) as note from mail_message group by res_id
                    ), master_merchant as (
                        select id from res_partner where contact_type ilike 'master_merchant' and active=true
                    )
                    SELECT
                        rp.name as "Tên Merchant",
                        ru.create_date as "Ngày kích hoạt Digistore Merchant",
                        rp.phone AS "Điện thoại",
                        rp.mobile AS "Di Động",
                        --rp.email AS "Email",
                        --rp.position AS "Chức vụ",
                        rp.status AS "Trạng thái",
                        rp.vat AS "Mã số thuế",
                        rp.merchant_id AS "Merchant ID",
                        rp.merchant_id AS "Merchant ID",
                        --lp.business_license_file_name AS "Giấy phép kinh doanh",
                        rpb.acc_holder_name AS "Tên chủ tài khoản",
                        rp.service_type AS "Loại dịch vụ",
                        rp.resgister_device AS  "Đăng ký thiết bị",
                        rpp.is_active as "Trạng thái EDC",
                        rpp.received_date as "Ngày nhận EDC",
                        rp.device_delivery_status AS "Trạng thái giao thiết bị",
                        tm.mid AS "Mid",
                        tm.tid AS "Tid",
                        tm.serial_no AS "Serial No",
                        STRING_AGG(DISTINCT rpb.acc_number, ', ') AS "Số tài khoản thanh toán"
                    FROM
                        res_partner rp
                    LEFT JOIN
                        res_users ru ON rp.id = ru.partner_id
                    LEFT JOIN
                        res_partner_bank rpb ON rp.id = rpb.partner_id
                    LEFT JOIN
                        res_bank rb ON rpb.bank_id = rb.id
                    LEFT JOIN
                    log_note lnt ON lnt.partner_id = rp.id
                    LEFT JOIN
                        maping_user sp ON rp.user_id = sp.res_user_id
                    LEFT JOIN
                        res_company rc ON rp.company_id = rc.id
                    LEFT JOIN
                        res_partner_pos rpp ON rp.id = rpp.merchant_id
                    LEFT JOIN
                        transaction_model tm ON tm.customer_id = rp.id
                    LEFT JOIN 
                        license_partner lp ON lp.partner_id = rp.id
                    WHERE
                        (ru.share = TRUE OR ru.share is null)
                    AND contact_type ilike 'merchant'
                        AND rp.active = TRUE
                    AND rp.id not in (select partner_id from res_company)
                    AND (rp.parent_id in (select * from master_merchant) OR (rp.parent_id is null AND rp.id not in (select * from master_merchant)))

                    GROUP BY
                        rp.id,
                        rp.name,
                        ru.create_date,
                        rp.contact_address_complete,
                        rp.phone,
                        rp.email,
                        rp.mobile,
                        rp.position,
                        rp.status,
                        rp.vat,
                        rp.merchant_id,
                        lp.business_license_file_name,
                        rpb.acc_holder_name,
                        rp.service_type,
                        rp.resgister_device,
                        rp.device_delivery_status,
                        tm.mid,
                        tm.tid,
                        tm.serial_no,
                        sp.name,
                        rc.name,
                    rpp.is_active,
                    rpp.received_date
                    ORDER BY
                        rp.name;
                    """
        cursor.execute(query)
        rows = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        # Chuyển dữ liệu thành DataFrame
        df = pd.DataFrame(rows, columns=column_names)

        # Xuất ra file Excel
        output_path = "/opt/airflow/out_data/exported_data.xlsx"  # Thay đường dẫn file phù hợp
        df.to_excel(output_path, index=False, engine='openpyxl')
        print(f"File Excel đã được xuất ra tại: {output_path}")
    except Exception as e:
        print(f"Lỗi xảy ra: {e}")
        raise

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 4, 15),  # Ngày bắt đầu DAG
}

# Định nghĩa DAG
dag = DAG(
    dag_id='export_postgres_to_excel',
    default_args=default_args,
    schedule_interval=None,  # Chạy DAG theo yêu cầu
)

# Task PythonOperator
export_task = PythonOperator(
    task_id='export_to_excel_task',
    python_callable=export_to_excel,
    dag=dag,
)
