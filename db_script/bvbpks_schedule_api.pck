CREATE OR REPLACE PACKAGE bvbpks_schedule_api IS

  -- Author  : TANNP
  -- Created : 16/07/2024 16:31:23
  -- Purpose : execute, get data purpose process schedule job

  PROCEDURE pr_truncate_table(i_table_name IN VARCHAR2);
  PROCEDURE pr_get_data_type
  (
    i_table_name IN VARCHAR2
   ,o_res        OUT SYS_REFCURSOR
  );
  PROCEDURE pr_get_col_name
  (
    i_table_name IN VARCHAR2
   ,o_res        OUT SYS_REFCURSOR
  );
  PROCEDURE pr_check_column_exist
  (
    i_table_name IN VARCHAR2
   ,i_column     IN VARCHAR2
   ,o_is_exist   OUT NUMBER
  );
  PROCEDURE pr_check_table_exist
  (
    i_table_name IN VARCHAR2
   ,o_is_exist   OUT NUMBER
  );
  PROCEDURE process_import_log
  (
    i_template_name IN VARCHAR2
   ,i_file_name     IN VARCHAR2
   ,o_file_id       OUT NUMBER
    
  );

  PROCEDURE update_import_status_log
  (
    i_status  IN NUMBER
   ,i_file_id IN NUMBER
  );
  PROCEDURE process_error_history
  (
    i_process_name IN VARCHAR2
   ,i_process_key  IN VARCHAR2
   ,i_error_msg    IN VARCHAR2
   ,i_note         IN VARCHAR2
   ,i_process_id   IN NUMBER DEFAULT -1
  );

  PROCEDURE schedule_history
  (
    i_task_id      NUMBER
   ,i_task_name    VARCHAR2
   ,i_start_date   DATE
   ,i_note         VARCHAR2 DEFAULT NULL
   ,i_is_completed NUMBER DEFAULT 0
  );
  FUNCTION schedule_frequency_fnc(i_Frequency IN VARCHAR2) RETURN VARCHAR2;
  FUNCTION schedule_day_of_week_fnc
  (
    i_Frequency   IN VARCHAR2
   ,i_Day_Of_Week IN NUMBER
  ) RETURN NUMBER;
  FUNCTION schedule_day_of_month_fnc
  (
    i_Frequency    IN VARCHAR2
   ,i_Day_Of_Month IN NUMBER
  ) RETURN NUMBER;

  PROCEDURE pr_get_task
  (
    i_run_time IN NUMBER
   ,i_task_id  IN NUMBER
   ,o_res      OUT SYS_REFCURSOR
  );

  PROCEDURE Insert_Schedule_Job_prc
  (
    i_Task_Order        IN NUMBER
   ,i_Task_Type         IN VARCHAR2
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Config_Key_Name   IN VARCHAR2 DEFAULT NULL
   ,i_Script            IN VARCHAR2 DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Output_Name       IN VARCHAR2 DEFAULT NULL
   ,i_src_Folder_Name   IN VARCHAR2 DEFAULT NULL
   ,i_src_File_Name     IN VARCHAR2 DEFAULT NULL
   ,i_src_File_Type     IN VARCHAR2 DEFAULT NULL
   ,i_dst_Folder_Name   IN VARCHAR2 DEFAULT NULL
   ,i_dst_File_Name     IN VARCHAR2 DEFAULT NULL
   ,i_dst_File_Type     IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 0
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_is_attachment     IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 0
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  );

  PROCEDURE Insert_Task_Execute_Prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Script            IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_is_attachment     IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 3600
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  );

  PROCEDURE Insert_Task_Python_Prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Script            IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 600
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  );

  PROCEDURE Insert_Task_Export_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Script            IN VARCHAR2
   ,i_Output_Name       IN VARCHAR2
   ,i_Folder_Name       IN VARCHAR2
   ,i_File_Name         IN VARCHAR2
   ,i_File_Type         IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 1
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_is_attachment     IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 1800
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  );

  PROCEDURE Insert_Task_Import_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Config_Key_Name   IN VARCHAR2
   ,i_Folder_Name       IN VARCHAR2
   ,i_File_Name         IN VARCHAR2
   ,i_File_Type         IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 1
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 1800
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  );
  PROCEDURE Insert_Task_sftp_Import_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Config_Key_Name   IN VARCHAR2
   ,i_src_Folder_Name   IN VARCHAR2
   ,i_src_File_Name     IN VARCHAR2
   ,i_src_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_dst_Folder_Name   IN VARCHAR2
   ,i_dst_File_Name     IN VARCHAR2
   ,i_dst_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 1
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 1800
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  );

  PROCEDURE Insert_Task_sftp_export_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Config_Key_Name   IN VARCHAR2
   ,i_src_Folder_Name   IN VARCHAR2
   ,i_src_File_Name     IN VARCHAR2
   ,i_src_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_dst_Folder_Name   IN VARCHAR2
   ,i_dst_File_Name     IN VARCHAR2
   ,i_dst_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Script            IN VARCHAR2
   ,i_Output_Name       IN VARCHAR2
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 1
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_is_attachment     IN NUMBER DEFAULT 0
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 1800
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  );

  PROCEDURE Insert_Task_sftp_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_task_Type         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Connection_String IN VARCHAR2
   ,i_src_Folder_Name   IN VARCHAR2
   ,i_src_File_Name     IN VARCHAR2
   ,i_src_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_dst_Folder_Name   IN VARCHAR2
   ,i_dst_File_Name     IN VARCHAR2
   ,i_dst_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Config_Key_Name   IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 1
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 300
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  );

  PROCEDURE Insert_Task_email_report_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Email             IN VARCHAR2
   ,i_Script            IN VARCHAR2
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 300
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  );

  PROCEDURE Insert_Task_email_attach_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Script            IN VARCHAR2
   ,i_Output_Name       IN VARCHAR2
   ,i_Folder_Name       IN VARCHAR2
   ,i_File_Name         IN VARCHAR2
   ,i_File_Type         IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 1800
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  );

END bvbpks_schedule_api;
/
CREATE OR REPLACE PACKAGE BODY bvbpks_schedule_api IS

  PROCEDURE pr_truncate_table(i_table_name IN VARCHAR2) AS
    l_exe_sql VARCHAR2(500);
  BEGIN
    l_exe_sql := 'TRUNCATE TABLE ' || i_table_name;
    EXECUTE IMMEDIATE l_exe_sql;
  
  END pr_truncate_table;

  PROCEDURE pr_get_data_type
  (
    i_table_name IN VARCHAR2
   ,o_res        OUT SYS_REFCURSOR
  ) AS
  BEGIN
    OPEN o_res FOR
      SELECT COLUMN_NAME
            ,DATA_TYPE
            ,DATA_LENGTH    AS MAX_LENGTH
            ,DATA_PRECISION AS PRECISION
            ,DATA_SCALE     AS SCALE
      FROM   user_tab_columns
      WHERE  table_name = i_table_name;
  
  END pr_get_data_type;

  PROCEDURE pr_get_col_name
  (
    i_table_name IN VARCHAR2
   ,o_res        OUT SYS_REFCURSOR
  ) AS
  BEGIN
    OPEN o_res FOR
      SELECT column_name FROM user_tab_columns WHERE table_name = i_table_name;
  
  END pr_get_col_name;

  PROCEDURE pr_check_column_exist
  (
    i_table_name IN VARCHAR2
   ,i_column     IN VARCHAR2
   ,o_is_exist   OUT NUMBER
  ) AS
    l_column_name VARCHAR2(50);
  BEGIN
    SELECT column_name
    INTO   l_column_name
    FROM   user_tab_columns
    WHERE  table_name = i_table_name
           AND column_name = i_column;
    IF i_column = l_column_name
    THEN
      o_is_exist := 1;
    ELSE
      o_is_exist := 0;
    END IF;
  EXCEPTION
    WHEN no_data_found THEN
      o_is_exist := 0;
    WHEN OTHERS THEN
      o_is_exist := 0;
  END pr_check_column_exist;

  PROCEDURE pr_check_table_exist
  (
    i_table_name IN VARCHAR2
   ,o_is_exist   OUT NUMBER
  ) AS
    l_table_name VARCHAR2(50);
  BEGIN
    SELECT table_name INTO l_table_name FROM all_tables WHERE table_name = i_table_name;
    IF i_table_name = l_table_name
    THEN
      o_is_exist := 1;
    ELSE
      o_is_exist := 0;
    END IF;
  EXCEPTION
    WHEN no_data_found THEN
      o_is_exist := 0;
    WHEN OTHERS THEN
      o_is_exist := 0;
  END pr_check_table_exist;

  PROCEDURE Process_Import_Log
  (
    i_Template_Name IN VARCHAR2
   ,i_File_Name     IN VARCHAR2
   ,o_File_Id       OUT NUMBER
    
  ) AS
  BEGIN
    INSERT INTO Vccb_Service_Import_Log
      (File_Id
      ,Template_Name
      ,File_Name
      ,Import_Date
      ,Is_Import)
    VALUES
      (Vccb_Schedule_Imp_Seq.Nextval
      ,i_Template_Name
      ,i_File_Name
      ,SYSDATE
      ,0)
    RETURNING File_Id INTO o_File_Id;
    COMMIT;
  END Process_Import_Log;

  PROCEDURE Update_Import_Status_Log
  (
    i_Status  IN NUMBER
   ,i_File_Id IN NUMBER
  ) AS
  BEGIN
    UPDATE Vccb_Service_Import_Log
    SET    Is_Import   = i_Status
          ,Import_Date = SYSDATE
    WHERE  File_Id = i_File_Id;
    COMMIT;
  END Update_Import_Status_Log;

  PROCEDURE process_error_history
  (
    i_process_name IN VARCHAR2
   ,i_process_key  IN VARCHAR2
   ,i_error_msg    IN VARCHAR2
   ,i_note         IN VARCHAR2
   ,i_process_id   IN NUMBER DEFAULT -1
  ) IS
  
  BEGIN
  
    INSERT INTO vccb_pro_error_history
      (process_name
      ,process_key
      ,error_msg
      ,note
      ,error_date
      ,process_id)
    VALUES
      (i_process_name
      ,i_process_key
      ,i_error_msg
      ,i_note
      ,SYSDATE
      ,i_process_id);
    COMMIT;
  
  END process_error_history;

  PROCEDURE schedule_history
  (
    i_task_id      NUMBER
   ,i_task_name    VARCHAR2
   ,i_start_date   DATE
   ,i_note         VARCHAR2 DEFAULT NULL
   ,i_is_completed NUMBER DEFAULT 0
  ) IS
    l_end_date DATE;
  BEGIN
    l_end_date := SYSDATE;
  
    INSERT INTO VCCB_SCHEDULE_JOB_HIS
      (ID
      ,TASK_NAME
      ,start_date
      ,end_date
      ,note
      ,is_completed
      ,log_date)
    VALUES
      (i_task_id
      ,i_task_name
      ,i_start_date
      ,l_end_date
      ,i_note
      ,i_is_completed
      ,SYSDATE);
    COMMIT;
  
  END schedule_history;
  FUNCTION Schedule_Frequency_Fnc(i_Frequency IN VARCHAR2) RETURN VARCHAR2 AS
    l_Frequency VARCHAR2(50);
  BEGIN
    l_Frequency := CASE
                     WHEN i_Frequency IS NULL THEN
                      'DAILY'
                     WHEN i_Frequency NOT IN ('DAILY', 'WEEKLY', 'MONTHLY') THEN
                      'DAILY'
                     ELSE
                      i_Frequency
                   END;
    RETURN l_Frequency;
  END Schedule_Frequency_Fnc;
  FUNCTION Schedule_Day_Of_Week_Fnc
  (
    i_Frequency   IN VARCHAR2
   ,i_Day_Of_Week IN NUMBER
  ) RETURN NUMBER AS
    l_Day_Of_Week NUMBER(2);
  BEGIN
    l_Day_Of_Week := CASE
                       WHEN Nvl(i_Frequency, '') <> 'WEEKLY' THEN
                        0
                       WHEN i_Day_Of_Week > 7 THEN
                        7 -- thu 7
                       WHEN i_Day_Of_Week < 1 THEN
                        1 -- chu nhat
                       ELSE
                        i_Day_Of_Week
                     END;
    RETURN l_Day_Of_Week;
  END Schedule_Day_Of_Week_Fnc;
  FUNCTION Schedule_Day_Of_Month_Fnc
  (
    i_Frequency    IN VARCHAR2
   ,i_Day_Of_Month IN NUMBER
  ) RETURN NUMBER AS
    l_Day_Of_Month NUMBER(2);
  BEGIN
    l_Day_Of_Month := CASE
                        WHEN Nvl(i_Frequency, '') <> 'MONTHLY' THEN
                         0
                        WHEN i_Day_Of_Month < 1 THEN
                         1
                        WHEN i_Day_Of_Month > 31 THEN
                         31
                        ELSE
                         i_Day_Of_Month
                      END;
    RETURN l_Day_Of_Month;
  END Schedule_Day_Of_Month_Fnc;

  PROCEDURE pr_get_task
  (
    i_run_time IN NUMBER
   ,i_task_id  IN NUMBER
   ,o_res      OUT SYS_REFCURSOR
  ) AS
  BEGIN
    OPEN o_res FOR
      SELECT job.Id AS "task_id"
             ,nvl(job.parent_task_id, -1) AS "parent_task_id"
             ,nvl(group_task.task_order, job.task_order) AS "task_order"
             ,job.task_type AS "task_type"
             ,job.task_name AS "task_name"
             ,job.run_time AS "run_time"
             ,job.config_key_name AS "config_key_name"
             ,CASE
               WHEN group_task.process_num IS NOT NULL THEN
                group_task.process_num
               WHEN Nvl(job.process_num, 1) > 3 THEN
                3
               WHEN Nvl(job.process_num, 1) < 1 THEN
                1
               ELSE
                Nvl(job.process_num, 1)
             END AS "process_num"
             ,job.Frequency AS "frequency"
             ,CASE
               WHEN To_Number(To_Char(Nvl(job.Day_Of_Week, 1))) < 1 THEN
                1
               WHEN To_Number(To_Char(Nvl(job.Day_Of_Week, 1))) > 7 THEN
                7
               ELSE
                Nvl(job.Day_Of_Week, 1)
             END AS "day_of_week"
             ,Nvl(job.Day_Of_Month, 1) AS "day_of_month"
             
             ,job.Script AS "script"
             ,job.connection_string AS "connection_string"
             ,job.output_name AS "output_name"
             ,job.src_folder_name AS "src_folder_name"
             ,job.src_file_name AS "src_file_name"
             ,lower(job.src_file_type) AS "src_file_type"
             ,dst_folder_name AS "dst_folder_name"
             ,dst_file_name AS "dst_file_name"
             ,Lower(job.dst_file_type) AS "dst_file_type"
             ,Nvl(job.Is_Header, 1) AS "is_header"
             ,Nvl(job.Is_Notification, 0) AS "is_notification"
             ,nvl(job.is_attachment, 0) AS "is_attachment"
             ,job.email AS "email"
             ,job.start_date AS "start_date"
             ,job.End_Date AS "end_date"
             ,job.task_time_out AS "task_time_out"
             ,job.retry_number AS "retry_number"
             ,job.sub_task_max_retry AS "sub_task_max_retry"
             ,CASE
               WHEN job.parent_task_id IS NULL THEN
                0
               ELSE
                1
             END AS "is_sub_task"
             ,CASE
               WHEN group_task.id IS NULL THEN
                0
               ELSE
                1
             END AS "is_frequency_task"
             ,CASE
               WHEN group_task.is_notify_fail IS NOT NULL THEN
                group_task.is_notify_fail
               ELSE
                0
             END AS "is_notify_fail"
             ,CASE
               WHEN group_task.is_notify_sucess IS NOT NULL THEN
                group_task.is_notify_sucess
               ELSE
                0
             END AS "is_notify_sucess"
      FROM   Vccb_Schedule_Job job
      LEFT   JOIN (SELECT ID
                         ,PARENT_TASK_ID
                         ,TASK_ORDER
                         ,PROCESS_NUM
                         ,IS_NOTIFY_FAIL
                         ,IS_NOTIFY_SUCESS
                   FROM   VCCB_JOB_frequency
                   WHERE  nvl(is_active, 0) = 1
                          AND To_Char(Start_Date, 'YYYYMMDD') <= To_Char(SYSDATE, 'YYYYMMDD')
                          AND To_Char(End_Date, 'YYYYMMDD') >= To_Char(SYSDATE, 'YYYYMMDD')
                          AND to_number(to_char(SYSDATE, 'HH24mi')) BETWEEN START_FROM_TIME AND
                          END_FROM_TIME
                          AND (to_char(i_task_id) = '-1' OR ID = i_task_id)
                   
                   ) group_task
      ON     job.ID = group_task.ID
      WHERE  Nvl(job.Active, 0) = 1
             AND To_Char(job.Start_Date, 'YYYYMMDD') <= To_Char(SYSDATE, 'YYYYMMDD')
             AND To_Char(job.End_Date, 'YYYYMMDD') >= To_Char(SYSDATE, 'YYYYMMDD')
             AND (job.Frequency = 'DAILY' OR
                  (job.Frequency = 'WEEKLY' AND job.Day_Of_Week = To_Number(To_Char(SYSDATE, 'D'))) OR
                  (job.Frequency = 'MONTHLY' AND (CASE
                    WHEN To_Number(To_Char(Nvl(job.Day_Of_Month, 1))) < 1 THEN
                     1
                    WHEN to_char(SYSDATE, 'MM') = '02'
                         AND Nvl(job.Day_Of_Month, 1) > 28
                         AND Nvl(job.Day_Of_Month, 1) <> To_Number(To_Char(Last_Day(SYSDATE), 'DD')) THEN
                     To_Number(To_Char(Last_Day(SYSDATE), 'DD'))
                    WHEN Nvl(job.Day_Of_Month, 1) > 31 THEN
                     to_number(To_Char(Last_Day(SYSDATE), 'DD'))
                    ELSE
                     Nvl(job.Day_Of_Month, 1)
                  END) = To_Number(To_Char(SYSDATE, 'DD'))))
             AND (job.run_time = i_run_time OR group_task.id IS NOT NULL)
             AND (to_char(i_task_id) = '-1' OR job.ID = i_task_id)
      ORDER  BY nvl(group_task.task_order, job.task_order);
  END pr_get_task;

  PROCEDURE Insert_Schedule_Job_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Type         IN VARCHAR2
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Config_Key_Name   IN VARCHAR2 DEFAULT NULL
   ,i_Script            IN VARCHAR2 DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Output_Name       IN VARCHAR2 DEFAULT NULL
   ,i_src_Folder_Name   IN VARCHAR2 DEFAULT NULL
   ,i_src_File_Name     IN VARCHAR2 DEFAULT NULL
   ,i_src_File_Type     IN VARCHAR2 DEFAULT NULL
   ,i_dst_Folder_Name   IN VARCHAR2 DEFAULT NULL
   ,i_dst_File_Name     IN VARCHAR2 DEFAULT NULL
   ,i_dst_File_Type     IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 0
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_is_attachment     IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 0
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  ) IS
  BEGIN
    INSERT INTO Vccb_Schedule_Job
      (Id
      ,Task_Order
      ,Task_Type
      ,Task_Name
      ,Run_Time
      ,Process_Num
      ,Frequency
      ,Day_Of_Week
      ,Day_Of_Month
      ,Config_Key_Name
      ,Script
      ,Connection_String
      ,Output_Name
      ,src_Folder_Name
      ,src_File_Name
      ,src_File_Type
      ,dst_Folder_Name
      ,dst_File_Name
      ,dst_File_Type
      ,Is_Header
      ,Is_Notification
      ,is_attachment
      ,Email
      ,Start_Date
      ,End_Date
      ,Active
      ,task_time_out
      ,retry_number
      ,Request_User
      ,Request_Date
      ,Process_User
      ,Process_Date
      ,Rec_Created_Date
      ,Rec_Updated_Date)
    VALUES
      (Vccb_Schedule_Id_Seq.Nextval
      ,i_task_Order
      ,i_task_Type
      ,i_task_Name
      ,i_Run_Time
      ,i_Process_Num
      ,i_Frequency
      ,i_Day_Of_Week
      ,i_Day_Of_Month
      ,i_Config_Key_Name
      ,i_Script
      ,i_Connection_String
      ,i_Output_Name
      ,i_src_Folder_Name
      ,i_src_File_Name
      ,i_src_File_Type
      ,i_dst_Folder_Name
      ,i_dst_File_Name
      ,i_dst_File_Type
      ,i_Is_Header
      ,i_Is_Notification
      ,i_is_attachment
      ,i_Email
      ,i_Start_Date
      ,i_End_Date
      ,i_Active
      ,i_task_time_out
      ,i_retry_number
      ,i_Request_User
      ,i_Request_Date
      ,i_Process_User
      ,i_Process_Date
      ,SYSDATE
      ,SYSDATE);
    COMMIT;
  
  END Insert_Schedule_Job_prc;

  PROCEDURE Insert_Task_Execute_Prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Script            IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_is_attachment     IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 3600
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  ) IS
    l_task_Type VARCHAR2(50) := 'EXECUTE_PROCEDURE';
    l_Frequency VARCHAR2(50);
  BEGIN
    l_Frequency := Schedule_Frequency_Fnc(i_Frequency => i_Frequency);
    Insert_Schedule_Job_prc(i_task_Order        => i_task_Order
                           ,i_task_Type         => l_task_Type
                           ,i_task_Name         => i_task_Name
                           ,i_Run_Time          => i_Run_Time
                           ,i_Process_Num       => i_Process_Num
                           ,i_Frequency         => l_Frequency
                           ,i_Start_Date        => i_Start_Date
                           ,i_End_Date          => i_End_Date
                           ,i_Day_Of_Week       => Schedule_Day_Of_Week_Fnc(i_Frequency   => l_Frequency
                                                                           ,i_Day_Of_Week => i_Day_Of_Week)
                           ,i_Day_Of_Month      => Schedule_Day_Of_Month_Fnc(i_Frequency    => l_Frequency
                                                                            ,i_Day_Of_Month => i_Day_Of_Month)
                           ,i_Config_Key_Name   => NULL
                           ,i_Script            => i_Script
                           ,i_Connection_String => i_Connection_String
                           ,i_Output_Name       => NULL
                           ,i_src_Folder_Name   => NULL
                           ,i_src_File_Name     => NULL
                           ,i_src_File_Type     => NULL
                           ,i_dst_Folder_Name   => NULL
                           ,i_dst_File_Name     => NULL
                           ,i_dst_File_Type     => NULL
                           ,i_Is_Header         => NULL
                           ,i_Is_Notification   => i_Is_Notification
                           ,i_is_attachment     => i_is_attachment
                           ,i_Email             => i_Email
                           ,i_Active            => i_Active
                           ,i_task_time_out     => i_task_time_out
                           ,i_retry_number      => i_retry_number
                           ,i_Request_User      => i_Request_User
                           ,i_Request_Date      => i_Request_Date
                           ,i_Process_User      => i_Process_User
                           ,i_Process_Date      => i_Process_Date);
  END Insert_Task_Execute_Prc;

  PROCEDURE Insert_Task_Python_Prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Script            IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 600
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  ) IS
    l_task_Type VARCHAR2(50) := 'EXECUTE_PYTHON';
    l_Frequency VARCHAR2(50);
  BEGIN
    l_Frequency := Schedule_Frequency_Fnc(i_Frequency => i_Frequency);
    Insert_Schedule_Job_prc(i_task_Order        => i_task_Order
                           ,i_task_Type         => l_task_Type
                           ,i_task_Name         => i_task_Name
                           ,i_Run_Time          => i_Run_Time
                           ,i_Process_Num       => i_Process_Num
                           ,i_Frequency         => l_Frequency
                           ,i_Start_Date        => i_Start_Date
                           ,i_End_Date          => i_End_Date
                           ,i_Day_Of_Week       => Schedule_Day_Of_Week_Fnc(i_Frequency   => l_Frequency
                                                                           ,i_Day_Of_Week => i_Day_Of_Week)
                           ,i_Day_Of_Month      => Schedule_Day_Of_Month_Fnc(i_Frequency    => l_Frequency
                                                                            ,i_Day_Of_Month => i_Day_Of_Month)
                           ,i_Config_Key_Name   => NULL
                           ,i_Script            => i_Script
                           ,i_Connection_String => i_Connection_String
                           ,i_Output_Name       => NULL
                           ,i_src_Folder_Name   => NULL
                           ,i_src_File_Name     => NULL
                           ,i_src_File_Type     => NULL
                           ,i_dst_Folder_Name   => NULL
                           ,i_dst_File_Name     => NULL
                           ,i_dst_File_Type     => NULL
                           ,i_Is_Header         => NULL
                           ,i_Is_Notification   => i_Is_Notification
                           ,i_is_attachment     => 0
                           ,i_Email             => i_Email
                           ,i_Active            => i_Active
                           ,i_task_time_out     => i_task_time_out
                           ,i_retry_number      => i_retry_number
                           ,i_Request_User      => i_Request_User
                           ,i_Request_Date      => i_Request_Date
                           ,i_Process_User      => i_Process_User
                           ,i_Process_Date      => i_Process_Date);
  END Insert_Task_Python_Prc;

  PROCEDURE Insert_Task_Export_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Script            IN VARCHAR2
   ,i_Output_Name       IN VARCHAR2
   ,i_Folder_Name       IN VARCHAR2
   ,i_File_Name         IN VARCHAR2
   ,i_File_Type         IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 1
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_is_attachment     IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 1800
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  ) IS
    l_task_Type VARCHAR2(50) := 'EXPORT';
    l_Frequency VARCHAR2(50);
    l_script    VARCHAR2(4000);
  BEGIN
    l_Frequency := Schedule_Frequency_Fnc(i_Frequency => i_Frequency);
    l_script := CASE
                  WHEN INSTR(UPPER(i_Script), 'SELECT') <= 0 THEN
                   'SELECT * FROM ' || i_Script || ';'
                  ELSE
                   i_Script
                END;
  
    Insert_Schedule_Job_prc(i_task_Order        => i_task_Order
                           ,i_task_Type         => l_task_Type
                           ,i_task_Name         => i_task_Name
                           ,i_Run_Time          => i_Run_Time
                           ,i_Process_Num       => i_Process_Num
                           ,i_Frequency         => l_Frequency
                           ,i_Start_Date        => i_Start_Date
                           ,i_End_Date          => i_End_Date
                           ,i_Day_Of_Week       => Schedule_Day_Of_Week_Fnc(i_Frequency   => l_Frequency
                                                                           ,i_Day_Of_Week => i_Day_Of_Week)
                           ,i_Day_Of_Month      => Schedule_Day_Of_Month_Fnc(i_Frequency    => l_Frequency
                                                                            ,i_Day_Of_Month => i_Day_Of_Month)
                           ,i_Config_Key_Name   => NULL
                           ,i_Script            => l_script
                           ,i_Connection_String => i_Connection_String
                           ,i_Output_Name       => i_Output_Name
                           ,i_src_Folder_Name   => NULL
                           ,i_src_File_Name     => NULL
                           ,i_src_File_Type     => NULL
                           ,i_dst_Folder_Name   => i_Folder_Name
                           ,i_dst_File_Name     => i_File_Name
                           ,i_dst_File_Type     => i_File_Type
                           ,i_Is_Header         => NULL
                           ,i_Is_Notification   => i_Is_Notification
                           ,i_is_attachment     => i_is_attachment
                           ,i_Email             => i_Email
                           ,i_Active            => i_Active
                           ,i_task_time_out     => i_task_time_out
                           ,i_retry_number      => i_retry_number
                           ,i_Request_User      => i_Request_User
                           ,i_Request_Date      => i_Request_Date
                           ,i_Process_User      => i_Process_User
                           ,i_Process_Date      => i_Process_Date);
  
  END Insert_Task_Export_prc;

  PROCEDURE Insert_Task_Import_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Config_Key_Name   IN VARCHAR2
   ,i_Folder_Name       IN VARCHAR2
   ,i_File_Name         IN VARCHAR2
   ,i_File_Type         IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 1
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 1800
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  ) IS
    l_task_Type VARCHAR2(50) := 'IMPORT';
    l_Frequency VARCHAR2(50);
  BEGIN
    l_Frequency := Schedule_Frequency_Fnc(i_Frequency => i_Frequency);
    Insert_Schedule_Job_prc(i_task_Order        => i_task_Order
                           ,i_task_Type         => l_task_Type
                           ,i_task_Name         => i_task_Name
                           ,i_Run_Time          => i_Run_Time
                           ,i_Process_Num       => i_Process_Num
                           ,i_Frequency         => l_Frequency
                           ,i_Start_Date        => i_Start_Date
                           ,i_End_Date          => i_End_Date
                           ,i_Day_Of_Week       => Schedule_Day_Of_Week_Fnc(i_Frequency   => l_Frequency
                                                                           ,i_Day_Of_Week => i_Day_Of_Week)
                           ,i_Day_Of_Month      => Schedule_Day_Of_Month_Fnc(i_Frequency    => l_Frequency
                                                                            ,i_Day_Of_Month => i_Day_Of_Month)
                           ,i_Config_Key_Name   => i_Config_Key_Name
                           ,i_Script            => NULL
                           ,i_Connection_String => i_Connection_String
                           ,i_Output_Name       => NULL
                           ,i_src_Folder_Name   => i_Folder_Name
                           ,i_src_File_Name     => i_File_Name
                           ,i_src_File_Type     => i_File_Type
                           ,i_dst_Folder_Name   => NULL
                           ,i_dst_File_Name     => NULL
                           ,i_dst_File_Type     => NULL
                           ,i_Is_Header         => NULL
                           ,i_Is_Notification   => i_Is_Notification
                           ,i_is_attachment     => 0
                           ,i_Email             => i_Email
                           ,i_Active            => i_Active
                           ,i_task_time_out     => i_task_time_out
                           ,i_retry_number      => i_retry_number
                           ,i_Request_User      => i_Request_User
                           ,i_Request_Date      => i_Request_Date
                           ,i_Process_User      => i_Process_User
                           ,i_Process_Date      => i_Process_Date);
  END Insert_Task_Import_prc;

  PROCEDURE Insert_Task_sftp_Import_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Config_Key_Name   IN VARCHAR2
   ,i_src_Folder_Name   IN VARCHAR2
   ,i_src_File_Name     IN VARCHAR2
   ,i_src_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_dst_Folder_Name   IN VARCHAR2
   ,i_dst_File_Name     IN VARCHAR2
   ,i_dst_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 1
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 1800
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  ) AS
    l_task_Type VARCHAR2(50) := 'SFTP_IMPORT';
    l_Frequency VARCHAR2(50);
  BEGIN
    l_Frequency := Schedule_Frequency_Fnc(i_Frequency => i_Frequency);
    Insert_Schedule_Job_prc(i_task_Order        => i_task_Order
                           ,i_task_Type         => l_task_Type
                           ,i_task_Name         => i_task_Name
                           ,i_Run_Time          => i_Run_Time
                           ,i_Process_Num       => i_Process_Num
                           ,i_Frequency         => l_Frequency
                           ,i_Start_Date        => i_Start_Date
                           ,i_End_Date          => i_End_Date
                           ,i_Day_Of_Week       => Schedule_Day_Of_Week_Fnc(i_Frequency   => l_Frequency
                                                                           ,i_Day_Of_Week => i_Day_Of_Week)
                           ,i_Day_Of_Month      => Schedule_Day_Of_Month_Fnc(i_Frequency    => l_Frequency
                                                                            ,i_Day_Of_Month => i_Day_Of_Month)
                           ,i_Config_Key_Name   => i_Config_Key_Name
                           ,i_Script            => NULL
                           ,i_Connection_String => i_Connection_String
                           ,i_Output_Name       => NULL
                           ,i_src_Folder_Name   => i_src_Folder_Name
                           ,i_src_File_Name     => i_src_File_Name
                           ,i_src_File_Type     => i_src_File_Type
                           ,i_dst_Folder_Name   => i_dst_Folder_Name
                           ,i_dst_File_Name     => i_dst_File_Name
                           ,i_dst_File_Type     => i_dst_File_Type
                           ,i_Is_Header         => NULL
                           ,i_Is_Notification   => i_Is_Notification
                           ,i_is_attachment     => 0
                           ,i_Email             => i_Email
                           ,i_Active            => i_Active
                           ,i_task_time_out     => i_task_time_out
                           ,i_retry_number      => i_retry_number
                           ,i_Request_User      => i_Request_User
                           ,i_Request_Date      => i_Request_Date
                           ,i_Process_User      => i_Process_User
                           ,i_Process_Date      => i_Process_Date);
  
  END Insert_Task_sftp_Import_prc;

  PROCEDURE Insert_Task_sftp_export_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Config_Key_Name   IN VARCHAR2
   ,i_src_Folder_Name   IN VARCHAR2
   ,i_src_File_Name     IN VARCHAR2
   ,i_src_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_dst_Folder_Name   IN VARCHAR2
   ,i_dst_File_Name     IN VARCHAR2
   ,i_dst_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Script            IN VARCHAR2
   ,i_Output_Name       IN VARCHAR2
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 1
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_is_attachment     IN NUMBER DEFAULT 0
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 1800
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  ) AS
    l_task_Type VARCHAR2(50) := 'SFTP_EXPORT';
    l_Frequency VARCHAR2(50);
  BEGIN
    l_Frequency := Schedule_Frequency_Fnc(i_Frequency => i_Frequency);
    Insert_Schedule_Job_prc(i_task_Order        => i_task_Order
                           ,i_task_Type         => l_task_Type
                           ,i_task_Name         => i_task_Name
                           ,i_Run_Time          => i_Run_Time
                           ,i_Process_Num       => i_Process_Num
                           ,i_Frequency         => l_Frequency
                           ,i_Start_Date        => i_Start_Date
                           ,i_End_Date          => i_End_Date
                           ,i_Day_Of_Week       => Schedule_Day_Of_Week_Fnc(i_Frequency   => l_Frequency
                                                                           ,i_Day_Of_Week => i_Day_Of_Week)
                           ,i_Day_Of_Month      => Schedule_Day_Of_Month_Fnc(i_Frequency    => l_Frequency
                                                                            ,i_Day_Of_Month => i_Day_Of_Month)
                           ,i_Config_Key_Name   => i_Config_Key_Name
                           ,i_Script            => i_Script
                           ,i_Connection_String => i_Connection_String
                           ,i_Output_Name       => i_Output_Name
                           ,i_src_Folder_Name   => i_src_Folder_Name
                           ,i_src_File_Name     => i_src_File_Name
                           ,i_src_File_Type     => i_src_File_Type
                           ,i_dst_Folder_Name   => i_dst_Folder_Name
                           ,i_dst_File_Name     => i_dst_File_Name
                           ,i_dst_File_Type     => i_dst_File_Type
                           ,i_Is_Header         => NULL
                           ,i_Is_Notification   => i_Is_Notification
                           ,i_is_attachment     => i_is_attachment
                           ,i_Email             => i_Email
                           ,i_Active            => i_Active
                           ,i_task_time_out     => i_task_time_out
                           ,i_retry_number      => i_retry_number
                           ,i_Request_User      => i_Request_User
                           ,i_Request_Date      => i_Request_Date
                           ,i_Process_User      => i_Process_User
                           ,i_Process_Date      => i_Process_Date);
  
  END Insert_Task_sftp_export_prc;

  PROCEDURE Insert_Task_sftp_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_task_Type         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Connection_String IN VARCHAR2
   ,i_src_Folder_Name   IN VARCHAR2
   ,i_src_File_Name     IN VARCHAR2
   ,i_src_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_dst_Folder_Name   IN VARCHAR2
   ,i_dst_File_Name     IN VARCHAR2
   ,i_dst_File_Type     IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Config_Key_Name   IN VARCHAR2 DEFAULT NULL
   ,i_Is_Header         IN NUMBER DEFAULT 1
   ,i_Is_Notification   IN NUMBER DEFAULT 0
   ,i_Email             IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 300
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  ) AS
    l_Frequency VARCHAR2(50);
  BEGIN
    l_Frequency := Schedule_Frequency_Fnc(i_Frequency => i_Frequency);
    Insert_Schedule_Job_prc(i_task_Order        => i_task_Order
                           ,i_task_Type         => i_task_Type
                           ,i_task_Name         => i_task_Name
                           ,i_Run_Time          => i_Run_Time
                           ,i_Process_Num       => i_Process_Num
                           ,i_Frequency         => l_Frequency
                           ,i_Start_Date        => i_Start_Date
                           ,i_End_Date          => i_End_Date
                           ,i_Day_Of_Week       => Schedule_Day_Of_Week_Fnc(i_Frequency   => l_Frequency
                                                                           ,i_Day_Of_Week => i_Day_Of_Week)
                           ,i_Day_Of_Month      => Schedule_Day_Of_Month_Fnc(i_Frequency    => l_Frequency
                                                                            ,i_Day_Of_Month => i_Day_Of_Month)
                           ,i_Config_Key_Name   => i_Config_Key_Name
                           ,i_Script            => NULL
                           ,i_Connection_String => i_Connection_String
                           ,i_Output_Name       => NULL
                           ,i_src_Folder_Name   => i_src_Folder_Name
                           ,i_src_File_Name     => i_src_File_Name
                           ,i_src_File_Type     => i_src_File_Type
                           ,i_dst_Folder_Name   => i_dst_Folder_Name
                           ,i_dst_File_Name     => i_dst_File_Name
                           ,i_dst_File_Type     => i_dst_File_Type
                           ,i_Is_Header         => NULL
                           ,i_Is_Notification   => i_Is_Notification
                           ,i_is_attachment     => 0
                           ,i_Email             => i_Email
                           ,i_Active            => i_Active
                           ,i_task_time_out     => i_task_time_out
                           ,i_retry_number      => i_retry_number
                           ,i_Request_User      => i_Request_User
                           ,i_Request_Date      => i_Request_Date
                           ,i_Process_User      => i_Process_User
                           ,i_Process_Date      => i_Process_Date);
  
  END Insert_Task_sftp_prc;

  PROCEDURE Insert_Task_email_report_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Email             IN VARCHAR2
   ,i_Script            IN VARCHAR2
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 300
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  ) AS
    l_task_Type VARCHAR2(50) := 'EMAIL_REPORT';
    l_Frequency VARCHAR2(50);
    l_script    VARCHAR2(4000);
  BEGIN
    l_Frequency := Schedule_Frequency_Fnc(i_Frequency => i_Frequency);
    l_script := CASE
                  WHEN INSTR(UPPER(i_Script), 'SELECT') <= 0 THEN
                   'SELECT * FROM ' || i_Script || ';'
                  ELSE
                   i_Script
                END;
  
    Insert_Schedule_Job_prc(i_task_Order        => i_task_Order
                           ,i_task_Type         => l_task_Type
                           ,i_task_Name         => i_task_Name
                           ,i_Run_Time          => i_Run_Time
                           ,i_Process_Num       => i_Process_Num
                           ,i_Frequency         => l_Frequency
                           ,i_Start_Date        => i_Start_Date
                           ,i_End_Date          => i_End_Date
                           ,i_Day_Of_Week       => Schedule_Day_Of_Week_Fnc(i_Frequency   => l_Frequency
                                                                           ,i_Day_Of_Week => i_Day_Of_Week)
                           ,i_Day_Of_Month      => Schedule_Day_Of_Month_Fnc(i_Frequency    => l_Frequency
                                                                            ,i_Day_Of_Month => i_Day_Of_Month)
                           ,i_Config_Key_Name   => NULL
                           ,i_Script            => l_script
                           ,i_Connection_String => i_Connection_String
                           ,i_Output_Name       => NULL
                           ,i_src_Folder_Name   => NULL
                           ,i_src_File_Name     => NULL
                           ,i_src_File_Type     => NULL
                           ,i_dst_Folder_Name   => NULL
                           ,i_dst_File_Name     => NULL
                           ,i_dst_File_Type     => NULL
                           ,i_Is_Header         => NULL
                           ,i_Is_Notification   => 1
                           ,i_is_attachment     => NULL
                           ,i_Email             => i_Email
                           ,i_Active            => i_Active
                           ,i_task_time_out     => i_task_time_out
                           ,i_retry_number      => i_retry_number
                           ,i_Request_User      => i_Request_User
                           ,i_Request_Date      => i_Request_Date
                           ,i_Process_User      => i_Process_User
                           ,i_Process_Date      => i_Process_Date);
  END Insert_Task_email_report_prc;
  PROCEDURE Insert_Task_email_attach_prc
  (
    i_task_Order        IN NUMBER
   ,i_task_Name         IN VARCHAR2
   ,i_Run_Time          IN NUMBER
   ,i_Process_Num       IN NUMBER
   ,i_Frequency         IN VARCHAR2
   ,i_Start_Date        IN DATE
   ,i_End_Date          IN DATE
   ,i_Script            IN VARCHAR2
   ,i_Output_Name       IN VARCHAR2
   ,i_Folder_Name       IN VARCHAR2
   ,i_File_Name         IN VARCHAR2
   ,i_File_Type         IN VARCHAR2 DEFAULT 'xlsx'
   ,i_Email             IN VARCHAR2
   ,i_Day_Of_Week       IN NUMBER DEFAULT NULL
   ,i_Day_Of_Month      IN NUMBER DEFAULT NULL
   ,i_Connection_String IN VARCHAR2 DEFAULT NULL
   ,i_Active            IN NUMBER DEFAULT 1
   ,i_task_time_out     IN NUMBER DEFAULT 1800
   ,i_retry_number      IN NUMBER DEFAULT 0
   ,i_Request_User      IN VARCHAR2 DEFAULT 'unitUser'
   ,i_Request_Date      IN DATE DEFAULT SYSDATE
   ,i_Process_User      IN VARCHAR2 DEFAULT 'sysUser'
   ,i_Process_Date      IN DATE DEFAULT SYSDATE
  ) AS
    l_task_Type VARCHAR2(50) := 'EMAIL_SEND_ATTACH_RPT';
    l_Frequency VARCHAR2(50);
    l_script    VARCHAR2(4000);
  BEGIN
    l_Frequency := Schedule_Frequency_Fnc(i_Frequency => i_Frequency);
    l_script := CASE
                  WHEN INSTR(UPPER(i_Script), 'SELECT') <= 0 THEN
                   'SELECT * FROM ' || i_Script || ';'
                  ELSE
                   i_Script
                END;
  
    Insert_Schedule_Job_prc(i_task_Order        => i_task_Order
                           ,i_task_Type         => l_task_Type
                           ,i_task_Name         => i_task_Name
                           ,i_Run_Time          => i_Run_Time
                           ,i_Process_Num       => i_Process_Num
                           ,i_Frequency         => l_Frequency
                           ,i_Start_Date        => i_Start_Date
                           ,i_End_Date          => i_End_Date
                           ,i_Day_Of_Week       => Schedule_Day_Of_Week_Fnc(i_Frequency   => l_Frequency
                                                                           ,i_Day_Of_Week => i_Day_Of_Week)
                           ,i_Day_Of_Month      => Schedule_Day_Of_Month_Fnc(i_Frequency    => l_Frequency
                                                                            ,i_Day_Of_Month => i_Day_Of_Month)
                           ,i_Config_Key_Name   => NULL
                           ,i_Script            => l_script
                           ,i_Connection_String => i_Connection_String
                           ,i_Output_Name       => NULL
                           ,i_src_Folder_Name   => NULL
                           ,i_src_File_Name     => NULL
                           ,i_src_File_Type     => NULL
                           ,i_dst_Folder_Name   => i_Folder_Name
                           ,i_dst_File_Name     => i_File_Name
                           ,i_dst_File_Type     => i_File_Type
                           ,i_Is_Header         => 1
                           ,i_Is_Notification   => 1
                           ,i_is_attachment     => 1
                           ,i_Email             => i_Email
                           ,i_Active            => i_Active
                           ,i_task_time_out     => i_task_time_out
                           ,i_retry_number      => i_retry_number
                           ,i_Request_User      => i_Request_User
                           ,i_Request_Date      => i_Request_Date
                           ,i_Process_User      => i_Process_User
                           ,i_Process_Date      => i_Process_Date);
  END Insert_Task_email_attach_prc;

END bvbpks_schedule_api;
/
