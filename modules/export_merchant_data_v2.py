from datetime import datetime, date
import psycopg2
import psycopg2.extras
import csv
import os
import io
import xlsxwriter

s3_endpoint_url = ""
s3_access_key = ""
s3_secret_key = ""
s3_bucket_name = "report"
report_file_name = "report.zip"
password_zip_file = "password"

connection_mms = psycopg2.connect(
    host="172.26.1.32", 
    database="bvbank_prod_mms", 
    user="readdw", 
    password="Vccb#1234", 
    port="5432"
)

connection_va = psycopg2.connect(
    host="172.26.1.32",
    database="va_service",
    user="readdw",
    password="Vccb#1234",
    port="5432",
)



try:
    cursor_mms = connection_mms.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor_va = connection_va.cursor(cursor_factory=psycopg2.extras.DictCursor)

    query_mms = """
        with maping_user as (
            select name, rs.id as res_user_id, rp as res_partner_id from res_partner rp left join res_users rs on rs.partner_id = rp.id
        ), log_note as (
            select res_id as partner_id, json_agg(body) as note from mail_message group by res_id
        ), master_merchant as (
            select id from res_partner where contact_type ilike 'master_merchant' and active=true
        )
        SELECT
            rp.name AS merchant_name,
            ru.create_date AS user_account_created_date,
            rp.contact_address_complete AS address,
            rp.phone AS phone,
            rp.mobile AS mobile,
            rp.email AS email,
            rp.position AS job_position,
            rp.status AS status,
            rp.vat AS tax_id,
            rp.merchant_id AS merchant_id,
            lp.business_license_file_name AS business_license_file_name,
            rpb.acc_holder_name AS bank_account_holder_name,
            rp.service_type AS service_type,
            rp.resgister_device AS register_device,
            rpp.is_active as pos_is_active,
            rpp.received_date as received_date,
            rp.device_delivery_status AS device_delivery_status,
                    tidmid.tid_domestic AS tid,
                    tidmid.mid_domestic AS mid,
                    rpp.name AS serial_no,
            STRING_AGG(DISTINCT rpb.acc_number, ', ') AS bank_account,
            json_agg(lnt.note) AS partner_notes,
            sp.name AS salesperson_name,
            rc.name AS company_name,
            json_agg(DISTINCT rpp.name) AS edc,
            rpb.verify_bank_date AS verify_bank_date
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
                    
            LEFT JOIN res_partner_pos_tidmid tidmid 
                    ON tidmid.partner_pos_id = rpp.id
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
            sp.name,
            rc.name,
            rpp.is_active,
            rpp.received_date,
            rpb.verify_bank_date,
                    rpp.name,
                    tidmid.tid_domestic,
                    tidmid.mid_domestic
        ORDER BY
            rp.name;
        """

    cursor_mms.execute(query_mms)
    query_va = (
        "SELECT va_account_no FROM public.atom_va_account WHERE bank_account_no = %s"
    )
    final_results = []
    column_mapping = {
        "merchant_name": "Tên Merchant",
        "user_account_created_date": "Ngày kích hoạt Digistore Merchant",
        "address": "Địa chỉ",
        "phone": "Điện thoại",
        "mobile": "Di động",
        "email": "Email",
        "job_position": "Chức vụ",
        "status": "Trạng thái",
        "tax_id": "Mã số thuế",
        "merchant_id": "Merchant ID",
        "business_license_file_name": "Giấy phép kinh doanh",
        "bank_account_holder_name": "Tên chủ tài khoản",
        "service_type": "Loại dịch vụ",
        "register_device": "Đăng ký thiết bị",
        "device_delivery_status": "Trạng thái giao thiết bị",
        "mid": "MID",
        "tid": "TID",
        "serial_no": "Serial No",
        "bank_account": "Số tài khoản thanh toán",
        # "qr_accounts": "Số tài khoản QR",
        "partner_notes": "Ghi chú nội bộ",
        "salesperson_name": "Nhân viên kinh doanh",
        "company_name": "Chi nhánh",
        "verify_bank_date": "Ngày kích hoạt QR",
        # "edc": "EDC",
        "pos_is_active": "Trạng thái EDC",
        "received_date": "Ngày nhận EDC",
    }
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # os.mkdir("output")
    file_name = f"/DATA/merchant_data_{current_time}.xlsx"

    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()
    headers = list(column_mapping.values())
    for col_num, header in enumerate(headers):
        worksheet.write(0, col_num, header)

    for row_num, row in enumerate(cursor_mms, start=1):
        bank_account = row[2]
        cursor_va.execute(query_va, (bank_account,))
 
        qr_account_results = cursor_va.fetchall()
        # qr_accounts_str = str(qr_account_results) if qr_account_results else ""
        for col_num, col_key in enumerate(column_mapping.keys()):
            cell = row[col_key]
            if isinstance(cell, list):
                cell = ", ".join(map(str, cell))
            if isinstance(cell, datetime):
                cell = cell.strftime("%Y-%m-%d %H:%M:%S")
            if isinstance(cell, date):
                cell = cell.strftime("%Y-%m-%d")
            worksheet.write(row_num, col_num, cell)
    workbook.close()

    # with open(file_name, "w", newline="", encoding="utf-8") as csvfile:
    #     csvwriter = csv.writer(csvfile)
    #     csvwriter.writerow(column_mapping.values())
    #     csvwriter.writerows(final_reults)

    
    
    
except Exception as e:
    connection_mms.rollback()
    connection_va.rollback()
    print(f"Lỗi: {e}")
finally:
    if connection_mms:
        cursor_mms.close()
        connection_mms.close()
    if connection_va:
        cursor_va.close()
        connection_va.close()