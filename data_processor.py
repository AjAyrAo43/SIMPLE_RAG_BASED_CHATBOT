# data_processor.py
import os
import pickle

# Dangerous mutable default argument bug
def process_user_items(item, items_list=[]):
    items_list.append(item)
    return items_list

# Command Injection Vulnerability
def ping_host(host_ip):
    # Executing raw user input in system shell
    os.system("ping -c 1 " + host_ip)

# Insecure Pickle Deserialization
def load_user_session(session_data):
    # Dangerous: loading untrusted pickle data
    return pickle.loads(session_data)

# Unclosed File Resource Leak
def write_log(message):
    f = open("app.log", "a")
    f.write(message)
    # File is never closed!
