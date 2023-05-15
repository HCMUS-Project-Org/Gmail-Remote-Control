import psutil
import os
import re
from . import shared_function as sf
#import shared_function as sf


def list_apps():
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

    result = ''
    for item in [(id, name, thread)for id, name, thread in zip(app_id, app_name, app_thread)]:
        result += ' - '.join(str(i) for i in item) + '\n'

    return result


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

    result = ''
    for item in [(id, name, thread) for id, name, thread in zip(proc_pid, proc_name, proc_thread)]:
        result += ' - '.join(str(i) for i in item) + '\n'

    return result


def kill(pid):
    command = None

    # check OS to specify the command
    if sf.check_os() == "linux":
        command = "kill -9 " + str(pid)
    else:
        command = "taskkill /F /PID " + str(pid)

    # Kill the process

    if os.system(command) != 0:
        return (f"Error: Failed to kill process with PID {pid}.\n")
    else:
        return f"Process with PID {pid} was killed.\n"


def start(name):
    if sf.check_os() == "linux":
        command = name
    else:
        command = "start " + name

    if os.system(command) != 0:
        return f"Error: Failed to start application with name {name}.\n"
    else:
        return f"Server started application with name {name}.\n"


def parse_msg(msg):
    command = [x for x in msg.split(" - ")]
    return command


def application_process(func):
    command = parse_msg(func)
    return_text = ""
    for item in command:
        result = ""

        if "Application" in item:
            result = "List of application\n" + "Id - Name - Thread\n" + list_apps()

        if "List" in item:
            result = "List of process\n" + "Id - Name - Thread\n" + list_processes()

        if "Kill" in item:
            try:
                id = re.search(r"id:(\d+)\]", item).group(1)
            except:
                return_text += f"Wrong format at {item}"
                continue

            result = "Kill process:\n" + kill(id)

        if "Start" in item:
            try:
                name = re.search(r'Start\[name:(.*)\]', item).group(1)
            except:
                return_text += f"Wrong format at {item}"
                continue

            result = "Start application:\n" + start(name)

        if result != "":
            return_text += "\n" + result

    return "<div class='mb-2'><b>Application/process management:</b> " + return_text + "</div>"
