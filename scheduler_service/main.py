import time
from datetime import datetime
from task_flow import TaskScheduler
# from main_test import run_job as test_run_job
# from main_test import _run_time_list as test_run_time_list


# print(_run_time_list)  
# ======================================================================================
# ++++++++++++++++++++++++++++++ Config start Schedule +++++++++++++++++++++++++++++++++
# ======================================================================================
_config_cycle_time = 5
_config_sleep_time = 5
_config_run_time_list = None

# ======================================================================================
# ++++++++++++++++++++++++++++++ End Config start Schedule +++++++++++++++++++++++++++++
# ======================================================================================
def test():
    print('test')
if __name__ == "__main__":
    with TaskScheduler(cycle_time=  _config_cycle_time, sleep_time= _config_sleep_time, run_time_list=_config_run_time_list) as task_schedule:
        try:
            task_schedule.scheduler.every(task_schedule.cycle_time).minutes.do(task_schedule.run, None)
            task_schedule.scheduler.every(5).minutes.do(test, None)
            # task_schedule.set_daily_schedule()
            while task_schedule.is_running:
                try:
                    task_schedule.scheduler.run_pending()

                    time.sleep(task_schedule.sleep_time)
                except KeyboardInterrupt:
                    task_schedule.logger.info(f'Schedule is Interrupted')
                    task_schedule.stop()
                    task_schedule.cleanup()
                    break
                except Exception as e:
                    task_schedule.logger.error(f'Schedule Run_Pending is Error: {e}')
                    task_schedule.stop()
                    task_schedule.cleanup()
                    break
        except Exception as e:
            task_schedule.logger.error(f'Schedule Starting is Error: {e}')
            task_schedule.stop()
            task_schedule.cleanup()
            # task_schedule.__exit__

