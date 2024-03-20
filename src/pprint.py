import os

def welcome():
    try:
        terminal_height = os.get_terminal_size().lines - 2
    except:
        terminal_height = 100
    print("\n" * terminal_height + "\033[H\033[J", end="")
    print("Welcome to the Hotel Reservation System!")

def invalid():
    print("Invalid input.\nType the code, full name, or underlined portion.\nE.g. 'FR1', 'Rooms and Rates', 'Rooms', or 'Rates'.\nCase insensitive.\n'Q' or 'Quit' to exit.")

def usr(extra=""):
    f = {"u": "\033[4m", "r": "\033[0m"}  # format: [underline, reset]
    spiel = (
        "Please select an option:\n\n"
        f"FR1: {f['u']}Rooms{f['r']} and {f['u']}Rates{f['r']}\n"
        f"FR2: {f['u']}Res{f['r']}ervations\n"
        f"FR3: Reservation {f['u']}Cancel{f['r']}lation\n"
        f"FR4: {f['u']}Detail{f['r']}ed Reservation {f['u']}Info{f['r']}rmation\n"
        f"{f['u']}Q{f['r']}uit\n"
    )
    usr = input(extra + spiel).lower()
    print("\033[H\033[J", end="")
    return usr


def fr1(data):
    print(data)