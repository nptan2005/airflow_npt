
import glob
import os

from task_flow.model.task import Task
from task_flow.taskConstant import TaskConstant
from task_flow.taskDispatcher import TaskDispatcher
from task_flow.taskScheduler import TaskScheduler
from task_flow.taskFactory import TaskFactory
from task_flow.task_utils import TaskUtils
from db_conn import ConnConstant,OracleConn
from data_kit import DataConstant
from conn_kit import ConnKitConstant
def main():
    try:
        

        tasks = [2,3,4,5,6]
        with TaskScheduler(5,5) as test:
            # for i in tasks:
            #     test.run(1615,i)
            test.run(1615)

        # from task_flow.task_data.task_data_load import TaskDataLoading

        # with TaskDataLoading() as t:
        #     data = t.get_tasks_from_db(1616)
        #     print(data)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()


