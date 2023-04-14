import psutil
import os
from shared_function import *


def list_apps():
    # TODO: check
    app_name = list()
    app_id = list()
    app_thread = list()

    cmd = 'powershell "gps | where {$_.mainWindowTitle} | select Description, ID, @{Name=\'ThreadCount\';Expression ={$_.Threads.Count}}'
    proc = os.popen(cmd).read().split('\n')
    tmp = list()
    for line in proc:
        if not line.isspace():
            tmp.append(line)
    tmp = tmp[3:]
    for line in tmp:
        try:
            arr = line.split(" ")
            if len(arr) < 3:
                continue
            if arr[0] == '' or arr[0] == ' ':
                continue

            name = arr[0]
            threads = arr[-1]
            ID = 0
            # iteration
            cur = len(arr) - 2
            for i in range(cur, -1, -1):
                if len(arr[i]) != 0:
                    ID = arr[i]
                    cur = i
                    break
            for i in range(1, cur, 1):
                if len(arr[i]) != 0:
                    name += ' ' + arr[i]
            app_name.append(name)
            app_id.append(ID)
            app_thread.append(threads)
        except:
            pass
    return app_name, app_id, app_thread


def list_processes():
    proc_pid = []
    proc_name = []
    proc_thread = []

    for process in psutil.process_iter():
        try:
            pid = process.pid
            name = process.name()
            threads = process.num_threads()

            proc_pid.append(pid)
            proc_name.append(name)
            proc_thread.append(str(threads))

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    return proc_pid, proc_name, proc_thread


def kill(pid):
    command = None

    # check OS to specify the command
    if check_os() == "linux":
        command = "kill -9 " + str(pid)
    else:
        command = "taskkill /F /PID " + str(pid)

    # Kill the process
    os.system(command)


def start(name):
    os.system(name)


def parse_msg(msg):
    command = [x.upper() for x in msg.split(" - ")]
    return command[1:]


if __name__ == '__main__':
    # TODO: done all functions -> need to process these function
    '''
    if linux -> list_app = list_proc
    '''

    # check_os()
    # # kill(30611)
    # start('chrome')
    # # commands = parse_msg("Application/Process - List")

    # for command in commands:
    #     print(command)
    #     res = 0
    #     ls1 = list()
    #     ls2 = list()
    #     ls3 = list()

    #     # 1-list
    #     if command == "LIST":
    #         if "APPLICATION" in commands:
    #             ls1, ls2, ls3 = list_apps()
    #         else:
    #             ls1, ls2 = list_processes()
    #         print("l1: ", ls1)
    #         print("l2: ", ls2)
    #     # 2 - kill
    #     elif command == "KILL":
    #         pass
    #     # 3 - clear
    #     elif command == "CLEAR":
    #         pass
    #     elif command == "START":
    #         pass
