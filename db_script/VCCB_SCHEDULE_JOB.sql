-- Create table
create table VCCB_SCHEDULE_JOB
(
  id                 NUMBER(18),
  parent_task_id     NUMBER(18),
  task_order         NUMBER(8),
  task_type          VARCHAR2(50),
  task_name          VARCHAR2(255),
  run_time           NUMBER(4),
  process_num        NUMBER(1),
  frequency          VARCHAR2(15),
  day_of_week        NUMBER(2),
  day_of_month       NUMBER(2),
  config_key_name    VARCHAR2(500),
  connection_string  VARCHAR2(255),
  script             VARCHAR2(4000),
  output_name        VARCHAR2(1000),
  src_folder_name    VARCHAR2(250),
  src_file_name      VARCHAR2(500),
  src_file_type      VARCHAR2(15),
  dst_folder_name    VARCHAR2(250),
  dst_file_name      VARCHAR2(500),
  dst_file_type      VARCHAR2(15),
  is_header          NUMBER(1),
  is_notification    NUMBER(1) default 0,
  is_attachment      NUMBER(1) default 0,
  email              VARCHAR2(1000),
  start_date         DATE,
  end_date           DATE,
  active             NUMBER(1) default 1,
  task_time_out      NUMBER(8) default 0,
  retry_number       NUMBER(2) default 0,
  sub_task_max_retry NUMBER(2) default 3,
  request_department VARCHAR2(255),
  request_user       VARCHAR2(255),
  request_date       DATE,
  process_user       VARCHAR2(255),
  process_date       DATE,
  rec_created_date   DATE,
  rec_updated_date   DATE
)
tablespace USERS
  pctfree 10
  initrans 1
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
-- Create/Recreate primary, unique and foreign key constraints 
alter table VCCB_SCHEDULE_JOB
  add constraint VCCB_SCHEDULE_JOB_UNIQUE unique (ID)
  using index 
  tablespace USERS
  pctfree 10
  initrans 2
  maxtrans 255
  storage
  (
    initial 64K
    next 1M
    minextents 1
    maxextents unlimited
  );
