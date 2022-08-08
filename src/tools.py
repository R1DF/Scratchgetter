# Imports
import os
from requests import get, ConnectionError

# Functions
def check_connection():
    try:
        get("http://api.scratch.mit.edu")
        return True

    except ConnectionError:
        return False

def insert_success(ld):
    print(ld["reusable"]["success"])

def insert_error(ld):
    print(ld["reusable"]["error"])

def await_enter(ld, to_exit=False):
    input(ld["reusable"]["enterToContinue"] + "\n" if not to_exit else ld["reusable"]["enterToExit"] + "\n")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def log(message):
    print(message, end=" ")

def break_line(amount=1):
    print("\n" * amount)
