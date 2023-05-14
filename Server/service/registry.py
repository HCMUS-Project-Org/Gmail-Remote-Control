'''
NOTE: Linux do not have REGISTRY
'''

import re
import winreg
import json
import os
from . import shared_function as sf
#import shared_function as sf


def parse_data(full_path):
    try:
        full_path = re.sub(r'/', r'\\', full_path)
        hive = re.sub(r'\\.*$', '', full_path)
        if not hive:
            raise ValueError('Invalid \'full_path\' param.')
        if len(hive) <= 4:
            if hive == 'HKLM':
                hive = 'HKEY_LOCAL_MACHINE'
            elif hive == 'HKCU':
                hive = 'HKEY_CURRENT_USER'
            elif hive == 'HKCR':
                hive = 'HKEY_CLASSES_ROOT'
            elif hive == 'HKU':
                hive = 'HKEY_USERS'
        reg_key = re.sub(r'^[A-Z_]*\\', '', full_path)
        reg_key = re.sub(r'\\[^\\]+$', '', reg_key)
        reg_value = re.sub(r'^.*\\', '', full_path)
        return hive, reg_key, reg_value
    except:
        return None, None, None


def dec_value(c):
    c = c.upper()
    if ord('0') <= ord(c) and ord(c) <= ord('9'):
        return ord(c) - ord('0')
    if ord('A') <= ord(c) and ord(c) <= ord('F'):
        return ord(c) - ord('A') + 10
    return 0


def str_to_bin(s):
    res = b""
    for i in range(0, len(s), 2):
        a = dec_value(s[i])
        b = dec_value(s[i + 1])
        res += (a * 16 + b).to_bytes(1, byteorder='big')
    return res


def str_to_dec(s):
    s = s.upper()
    res = 0
    for i in range(0, len(s)):
        v = dec_value(s[i])
        res = res*16 + v
    return res


'''
Get a value of a registry key
Input: 
    full_path = <full_path> + r'\\' + <name_value>
        <full_path>: full path of the registry key
        <name_value>: name of the value of key
Usage: 
    res = get_value(full_path + r'\\' + name_value)
'''


def get_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(
            getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
        value_of_value, value_type = winreg.QueryValueEx(
            opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return f'"{full_path}" value is "{value_of_value}"'
    except:
        return "Server can not read value"


'''
Set a value of a registry key
Input: 
    full_path = <full_path> + r'\\' + <name_value>
        <full_path>: full path of the registry key
        <name_value>: name of the value of key
    value: value of the value of key
    value_type: type of the value of key
Usage: 
    res = get_value(full_path + r'\\' + name_value, value, value_type)
'''


def set_value(full_path, value, value_type):
    value_list = parse_data(full_path)
    try:
        winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1])
        opened_key = winreg.OpenKey(
            getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
        if 'REG_BINARY' in value_type:
            if len(value) % 2 == 1:
                value += '0'
            value = str_to_bin(value)
        if 'REG_DWORD' in value_type:
            if len(value) > 8:
                value = value[:8]
            value = str_to_dec(value)
        if 'REG_QWORD' in value_type:
            if len(value) > 16:
                value = value[:16]
            value = str_to_dec(value)

        winreg.SetValueEx(opened_key, value_list[2], 0, getattr(
            winreg, value_type), value)
        winreg.CloseKey(opened_key)
        return "Server set value successfully"
    except:
        return "Server set value fail"


def create_key(full_path):
    value_list = parse_data(full_path)
    try:
        winreg.CreateKey(
            getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
        return f"Server created new key at {full_path}"
    except:
        return "Server cannot create new key"


def delete_key(full_path):
    value_list = parse_data(full_path)
    try:
        winreg.DeleteKey(
            getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
        return f"Server deleted key at {full_path}"
    except:
        return "Server cannot delete key"


def parse_msg(msg):
    command = [x for x in msg.split(" - ")]
    return command


def parse_cmd(item):
    try:
        path = re.search(r'path:(.*?)(,|\])', item)
        path = path.group(1) if path else None

        name = re.search(r'name:(.*?)(,|\])', item)
        name = name.group(1) if name else None

        value = re.search(r'value:(.*?)(,|\])', item)
        value = value.group(1) if value else None

        value_type = re.search(r"type:(.*?)(,|\])", item)
        value_type = value_type.group(1) if value_type else None

        return path, name, value, value_type
    except:
        return False


def registry(msg):
    if sf.check_os() != "window":
        return f"Server running on {sf.check_os()}"
    command = parse_msg(msg)
    return_text = ""

    for item in command:
        path, name, value, value_type = parse_cmd(item)
        result = ''
        if path == False:
            return_text += f"Wrong format at {item}"
            continue

        if "Get value" in item:
            result = "<p>Get registry value</p>\n" + \
                get_value(path + '\\' + name)

        elif "Set value" in item:
            print(value)
            result = "<p>Set registry value</p>\n" + \
                set_value(path + '\\' + name, value, value_type)

        elif "Create key" in item:
            result = "<p>Create new registry key</p>\n" + \
                create_key(path)

        elif "Delete key" in item:
            result = "<p>Delete registry key</p>\n" + \
                delete_key(path + '\\')

        if result != '':
            return_text += "\n" + result

    return "</br><b>Registry management:</b>\n" + return_text

