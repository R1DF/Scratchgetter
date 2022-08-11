# Imports
import os
from requests import get, ConnectionError
from random import choice
from rich import print as rprint

# Functions
def validate_key(key):
    # "SCRGTR_NANBNANB_ABACADADACACABAD_SASBSDSCSCSDq"
    # "SCRGTR_NANBNANB_ABAADADADAADAADABAD_SASBSDSCSCSDq"
    # "SCRGTR_0909_ARrrRRAr_()!$$!q"
    if len(key) != 28:
        return False
    try:
        NA = key[7]
        NB = key[8]
        AB = key[12]
        AC = key[13]
        AD = key[14]
        SA = key[21]
        SB = key[22]
        SC = key[24]
        SD = key[23]

        key = key[7:-1].replace(
            NA, "NA"
        ).replace(
            NB, "NB",
        ).replace(
            AB, "AB"
        ).replace(
            AC, "AC"
        ).replace(
            AD, "AD"
        ).replace(
            SA, "SA"
        ).replace(
            SB, "SB"
        ).replace(
            SC, "SC"
        ).replace(
            SD, "SD"
        )
        return key == "NANBNANB_ABACADADACACABAD_SASBSDSCSCSD"
    except Exception:
        return False

def randomize_key():
    numbers = [str(x) for x in list(range(10))] # I am smart
    letters = [chr(x) for x in list(range(65, 91))] + [chr(x) for x in list(range(97, 123))]
    symbols = ["!", "@", "$", "%", "^", "&", "*", "?", "(", ")", "-", "+"]

    # Removing anomalies
    for letter in ["N", "A", "B", "C", "D", "S"]:
        letters.remove(letter)

    # Getting replacers
    replacers = []
    for i in range(2):
        added = choice(numbers)
        replacers.append(added)
        numbers.remove(added)

    for i in range(3):
        added = choice(letters)
        replacers.append(added)
        letters.remove(added)

    for i in range(4):
        added = choice(symbols)
        replacers.append(added)
        symbols.remove(added)

    # It's time.
    key = "SCRGTR_NANBNANB_ABACADADACACABAD_SASBSDSCSCSDq"
    key = key.replace(
        "SCRGTR", choice(["scrgtr", "S|CRGTR"])
    ).replace(
        "NA", replacers[0]
    ).replace(
        "NB", replacers[1]
    ).replace(
        "AB", replacers[2]
    ).replace(
        "AC", replacers[3]
    ).replace(
        "AD", replacers[4]
    ).replace(
        "SA", replacers[5]
    ).replace(
        "SB", replacers[6]
    ).replace(
        "SC", replacers[7]
    ).replace(
        "SD", replacers[8]
    ).replace(
        "|", ""
    )

    return key

def check_connection():
    try:
        get("http://api.scratch.mit.edu")
        return True

    except ConnectionError:
        return False

def insert_success(ld):
    rprint("[green]" + ld["reusable"]["success"])

def insert_error(ld):
    rprint("[red]" + ld["reusable"]["error"])

def await_enter(ld, to_exit=False):
    input(ld["reusable"]["enterToContinue"] + "\n" if not to_exit else ld["reusable"]["enterToExit"] + "\n")

def await_retry(ld):
    input(ld["reusable"]["enterToRetry"] + "\n")

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def log(message):
    rprint("[yellow]" + message, end=" ")

def break_line(amount=1):
    print("\n" * amount)
