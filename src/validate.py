import re
from datetime import datetime

def quit(usr):
    return usr == "q" or usr == "quit"

def fr1(usr):
    return usr == "fr1" or usr == "rooms and rates" or usr == "rooms" or usr == "rates"

def fr2(usr):
    return usr == "fr2" or usr == "reservations" or usr == "res"

def fr2_req(choices):
    alpha = {"first", "last", "room", "bed"}
    date = {"start", "end"}
    num = {"children", "adults"}
    for key in choices:
        if key in alpha:
            if choices[key].isalpha():
                choices[key] = choices[key].upper()
            else:
                raise ValueError("Invalid input in choices", key, choices[key])
        elif key in date:
            if not re.match(r"\d{4}-\d{2}-\d{2}", choices[key]) or not is_valid_date(choices[key], "future"):
                raise ValueError("Invalid date format. Please use YYYY-MM-DD format and make sure date is in the future.")
        elif key in num:
            if not choices[key].isdigit():
                raise ValueError("Invalid input in choices", key, choices[key])
        else:
            raise ValueError("Invalid input in choices", key, choices[key])
    if not is_valid_date(choices["start"]) < is_valid_date(choices["end"]):
        raise ValueError("Start date must be before end date.", choices["start"], choices["end"])
    return choices

def is_valid_date(date_str, when=""):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()
        if when == "future" and date < datetime.now().date():
            return False
        return date
    except ValueError:
        return False

def fr3(usr):
    return usr == "fr3" or usr == "reservation cancellation" or usr == "cancel"

def fr3_req(code):
    return code is not None and code.isdigit()

def fr3_confirm(usr):
    return usr == "YES" or usr == "Y" or usr == "NO" or usr == "N"

def fr4(usr):
    return usr == "fr4" or usr == "detailed reservation information" or usr == "detail" or usr == "info"

def fr5(usr):
    return usr == "fr5" or usr == "revenue" or usr == "rev"
