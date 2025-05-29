SET search_path TO task_flow;
CREATE OR REPLACE FUNCTION pg_nvl(input_val ANYELEMENT, default_val ANYELEMENT)
RETURNS ANYELEMENT AS $$
BEGIN
    RETURN COALESCE(input_val, default_val);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Helper function to mimic Oracle's TO_NUMBER for simple cases
CREATE OR REPLACE FUNCTION pg_to_number(input_text TEXT)
RETURNS INTEGER AS $$
BEGIN
    RETURN input_text::INTEGER;
EXCEPTION
    WHEN invalid_text_representation THEN
        RETURN NULL; -- Or handle error as needed
END;
$$ LANGUAGE plpgsql IMMUTABLE;


-- Equivalent of Oracle's pr_get_task
-- This function will query the 'custom_task_definitions' table
CREATE OR REPLACE FUNCTION get_tasks_for_dag(
    p_run_time INTEGER,
    p_task_id INTEGER DEFAULT -1 -- -1 means all relevant tasks for the run_time
)
RETURNS TABLE (
    task_id INTEGER,
    parent_task_id INTEGER,
    task_order INTEGER,
    task_type VARCHAR(50),
    task_name VARCHAR(255),
    run_time INTEGER,
    config_key_name VARCHAR(500),
    process_num INTEGER,
    frequency VARCHAR(50),
    day_of_week INTEGER,
    day_of_month INTEGER,
    script TEXT,
    connection_string VARCHAR(255),
    output_name TEXT,
    src_folder_name VARCHAR(250),
    src_file_name VARCHAR(500),
    src_file_type VARCHAR(50),
    dst_folder_name VARCHAR(250),
    dst_file_name VARCHAR(500),
    dst_file_type VARCHAR(50),
    is_header BOOLEAN,
    is_notification BOOLEAN,
    is_attachment BOOLEAN,
    email TEXT,
    start_date TIMESTAMP,
    end_date TIMESTAMP,
    task_time_out INTEGER,
    retry_number INTEGER,
    sub_task_max_retry INTEGER,
    is_sub_task BOOLEAN,
    -- Fields for is_frequency_task, is_notify_fail, is_notify_sucess would typically
    -- come from a related table or be part of the task_definition itself if simpler.
    -- For this conversion, we'll assume they might be part of custom_task_definitions
    -- or a simplified logic. The VCCB_JOB_frequency table logic is complex to replicate directly here.
    -- We will add placeholder columns for now, assuming they might be added to custom_task_definitions
    is_frequency_task BOOLEAN, -- Placeholder
    is_notify_fail BOOLEAN,    -- Placeholder
    is_notify_sucess BOOLEAN   -- Placeholder
)
AS $$
BEGIN
    -- The original Oracle query joins with VCCB_JOB_frequency for overriding certain values.
    -- Replicating that join and its complex time logic exactly requires VCCB_JOB_frequency
    -- to also be migrated and its logic adapted.
    -- This simplified version queries 'custom_task_definitions' directly
    -- and applies basic filtering similar to the original query's WHERE clause.

    RETURN QUERY
    SELECT
        td.id AS task_id,
        pg_nvl(td.parent_task_id, -1) AS parent_task_id,
        pg_nvl(td.task_order, 0) AS task_order, -- Simplified: not joining with a frequency override table
        td.task_type,
        td.task_name,
        td.run_time,
        td.config_key_name,
        CASE
            WHEN pg_nvl(td.process_num, 1) > 3 THEN 3
            WHEN pg_nvl(td.process_num, 1) < 1 THEN 1
            ELSE pg_nvl(td.process_num, 1)
        END AS process_num, -- Simplified
        td.frequency,
        CASE
            WHEN pg_to_number(pg_nvl(td.day_of_week, 1)::TEXT) < 1 THEN 1
            WHEN pg_to_number(pg_nvl(td.day_of_week, 1)::TEXT) > 7 THEN 7
            ELSE pg_nvl(td.day_of_week, 1)
        END AS day_of_week,
        pg_nvl(td.day_of_month, 1) AS day_of_month,
        td.script,
        td.connection_string,
        td.output_name,
        td.src_folder_name,
        td.src_file_name,
        lower(td.src_file_type) AS src_file_type,
        td.dst_folder_name,
        td.dst_file_name,
        lower(td.dst_file_type) AS dst_file_type,
        pg_nvl(td.is_header, FALSE) AS is_header,
        pg_nvl(td.is_notification, FALSE) AS is_notification,
        pg_nvl(td.is_attachment, FALSE) AS is_attachment,
        td.email,
        td.start_date,
        td.end_date,
        td.task_time_out,
        td.retry_number,
        td.sub_task_max_retry,
        CASE
            WHEN td.parent_task_id IS NULL THEN FALSE
            ELSE TRUE
        END AS is_sub_task,
        FALSE AS is_frequency_task, -- Placeholder: requires VCCB_JOB_frequency logic
        FALSE AS is_notify_fail,    -- Placeholder
        FALSE AS is_notify_sucess   -- Placeholder
    FROM
        airflow.custom_task_definitions td -- Assuming schema is 'airflow'
    WHERE
        pg_nvl(td.active, FALSE) = TRUE
        AND td.start_date <= CURRENT_TIMESTAMP
        AND td.end_date >= CURRENT_TIMESTAMP
        AND (
            td.frequency = 'DAILY' OR
            (td.frequency = 'WEEKLY' AND td.day_of_week = EXTRACT(ISODOW FROM CURRENT_TIMESTAMP)) OR -- ISODOW: Mon=1 to Sun=7
            (td.frequency = 'MONTHLY' AND
                (CASE
                    WHEN pg_to_number(pg_nvl(td.day_of_month, 1)::TEXT) < 1 THEN 1
                    WHEN EXTRACT(MONTH FROM CURRENT_TIMESTAMP) = 2 AND pg_nvl(td.day_of_month, 1) > 28
                         AND pg_nvl(td.day_of_month, 1) <> EXTRACT(DAY FROM (date_trunc('MONTH', CURRENT_TIMESTAMP) + INTERVAL '1 MONTH - 1 DAY')) THEN
                        EXTRACT(DAY FROM (date_trunc('MONTH', CURRENT_TIMESTAMP) + INTERVAL '1 MONTH - 1 DAY'))::INTEGER
                    WHEN pg_nvl(td.day_of_month, 1) > 31 THEN
                        EXTRACT(DAY FROM (date_trunc('MONTH', CURRENT_TIMESTAMP) + INTERVAL '1 MONTH - 1 DAY'))::INTEGER
                    ELSE pg_nvl(td.day_of_month, 1)
                END) = EXTRACT(DAY FROM CURRENT_TIMESTAMP)::INTEGER
            )
        )
        AND (td.run_time = p_run_time) -- Simplified: not considering frequency override table for run_time
        AND (p_task_id = -1 OR td.id = p_task_id)
    ORDER BY
        pg_nvl(td.task_order, 0); -- Simplified ordering
END;
$$ LANGUAGE plpgsql;

-- Equivalent of Oracle's Insert_Schedule_Job_prc
CREATE OR REPLACE PROCEDURE insert_schedule_job_pg(
    p_task_order INTEGER,
    p_task_type VARCHAR(50),
    p_task_name VARCHAR(255),
    p_run_time INTEGER,
    p_process_num INTEGER,
    p_frequency VARCHAR(50),
    p_start_date TIMESTAMP,
    p_end_date TIMESTAMP,
    p_day_of_week INTEGER DEFAULT NULL,
    p_day_of_month INTEGER DEFAULT NULL,
    p_config_key_name VARCHAR(500) DEFAULT NULL,
    p_script TEXT DEFAULT NULL,
    p_connection_string VARCHAR(255) DEFAULT NULL,
    p_output_name TEXT DEFAULT NULL,
    p_src_folder_name VARCHAR(250) DEFAULT NULL,
    p_src_file_name VARCHAR(500) DEFAULT NULL,
    p_src_file_type VARCHAR(50) DEFAULT NULL,
    p_dst_folder_name VARCHAR(250) DEFAULT NULL,
    p_dst_file_name VARCHAR(500) DEFAULT NULL,
    p_dst_file_type VARCHAR(50) DEFAULT NULL,
    p_is_header BOOLEAN DEFAULT FALSE,
    p_is_notification BOOLEAN DEFAULT FALSE,
    p_is_attachment BOOLEAN DEFAULT FALSE,
    p_email TEXT DEFAULT NULL,
    p_active BOOLEAN DEFAULT TRUE,
    p_task_time_out INTEGER DEFAULT 0,
    p_retry_number INTEGER DEFAULT 0,
    p_sub_task_max_retry INTEGER DEFAULT 3, -- Added from TaskDefinition model
    p_request_department VARCHAR(255) DEFAULT 'unitUser',
    p_request_user VARCHAR(255) DEFAULT 'unitUser',
    p_request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    p_process_user VARCHAR(255) DEFAULT 'sysUser',
    p_process_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- p_parent_task_id is missing from Oracle proc, but in our table. Assume it's set separately or via UI.
)
AS $$
BEGIN
    INSERT INTO airflow.custom_task_definitions (
        task_order, task_type, task_name, run_time, process_num, frequency,
        start_date, end_date, day_of_week, day_of_month, config_key_name,
        script, connection_string, output_name, src_folder_name, src_file_name,
        src_file_type, dst_folder_name, dst_file_name, dst_file_type,
        is_header, is_notification, is_attachment, email, active, task_time_out,
        retry_number, sub_task_max_retry,
        request_department, request_user, request_date, process_user, process_date,
        created_at, updated_at
        -- parent_task_id needs to be handled if this proc is used for all inserts
    ) VALUES (
        p_task_order, p_task_type, p_task_name, p_run_time, p_process_num, p_frequency,
        p_start_date, p_end_date, p_day_of_week, p_day_of_month, p_config_key_name,
        p_script, p_connection_string, p_output_name, p_src_folder_name, p_src_file_name,
        p_src_file_type, p_dst_folder_name, p_dst_file_name, p_dst_file_type,
        p_is_header, p_is_notification, p_is_attachment, p_email, p_active, p_task_time_out,
        p_retry_number, p_sub_task_max_retry,
        p_request_department, p_request_user, p_request_date, p_process_user, p_process_date,
        CURRENT_TIMESTAMP, CURRENT_TIMESTAMP
    );
END;
$$ LANGUAGE plpgsql;

-- Note: The various other Insert_Task_*_Prc procedures from your Oracle package
-- were essentially wrappers calling Insert_Schedule_Job_prc with specific
-- task_types and default values. You can recreate these as separate PostgreSQL
-- procedures calling insert_schedule_job_pg if needed, or handle this logic
-- in your Python code/Airflow plugin UI when preparing data for insertion.

-- Example of a wrapper, e.g., for Insert_Task_Execute_Prc
CREATE OR REPLACE PROCEDURE insert_task_execute_pg (
    p_task_order INTEGER,
    p_task_name VARCHAR(255),
    p_script TEXT,
    p_run_time INTEGER,
    p_process_num INTEGER,
    p_frequency VARCHAR(50),
    p_start_date TIMESTAMP,
    p_end_date TIMESTAMP,
    p_day_of_week INTEGER DEFAULT NULL,
    p_day_of_month INTEGER DEFAULT NULL,
    p_connection_string VARCHAR(255) DEFAULT NULL,
    p_is_notification BOOLEAN DEFAULT FALSE,
    p_is_attachment BOOLEAN DEFAULT FALSE, -- Oracle version had this
    p_email TEXT DEFAULT NULL,
    p_active BOOLEAN DEFAULT TRUE,
    p_task_time_out INTEGER DEFAULT 3600,
    p_retry_number INTEGER DEFAULT 0
    -- Other audit params can be added with defaults
)
AS $$
DECLARE
    v_task_type VARCHAR(50) := 'EXECUTE_PROCEDURE'; -- Or map to Airflow operator type like 'PostgresOperator'
    v_frequency VARCHAR(50);
BEGIN
    -- Simplified frequency logic from Oracle package
    v_frequency := CASE
                       WHEN p_frequency IS NULL THEN 'DAILY'
                       WHEN p_frequency NOT IN ('DAILY', 'WEEKLY', 'MONTHLY') THEN 'DAILY'
                       ELSE p_frequency
                   END;

    CALL insert_schedule_job_pg(
        p_task_order        => p_task_order,
        p_task_type         => v_task_type,
        p_task_name         => p_task_name,
        p_run_time          => p_run_time,
        p_process_num       => p_process_num,
        p_frequency         => v_frequency,
        p_start_date        => p_start_date,
        p_end_date          => p_end_date,
        p_day_of_week       => p_day_of_week, -- Add Oracle's day_of_week/month logic if needed here
        p_day_of_month      => p_day_of_month,
        p_script            => p_script,
        p_connection_string => p_connection_string,
        p_is_notification   => p_is_notification,
        p_is_attachment     => p_is_attachment,
        p_email             => p_email,
        p_active            => p_active,
        p_task_time_out     => p_task_time_out,
        p_retry_number      => p_retry_number
        -- Fill other params with NULLs or defaults as in Oracle's Insert_Task_Execute_Prc
    );
END;
$$ LANGUAGE plpgsql;