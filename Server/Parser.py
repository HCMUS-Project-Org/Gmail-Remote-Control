# import service.capture_screen as cs
# import service.capture_webcam as cw
# import service.mac_address as mac

msg = '''Key logger - Hook - Print
Capture Screen
Capture Webcam
MAC address
Directory tree - Show[path:C:/, level:2] - Copy file[source:C:/, destination:C:/] -Send file to folder[source:C:/, destination:C:/] - Delete file[path:C:/]
Shutdown/Logout - Shutdown - Logout
Application/Process - Application - List - Kill[id:3] - Start[id:notepad.exe]'''

def action1(default_value=None):
    print(1)
def action2(default_value=None):
    print(2)
def action3(default_value=None):
    print(3)    

action_map = {
    "Key logger": action1,
    "Capture Screen": action2,
    "Capture Webcam": action3,
    "MAC address": action1,
    "Directory tree": action2,
    "Shutdown/Logout": action3,
    "Application/Process": action1,
}

def parse_msg(msg):
    options = []
    # Separate each line into main part and sub part
    for line in msg.split('\n'):
        options.append(line.split(' - ', 1))
    
    return options


def function(msg):
    options = parse_msg(msg)
    for func in options:
        if (len(func) == 1):
            action_map[func[0]]()
        else: 
            action_map[func[0]](func[1])



function(msg)






