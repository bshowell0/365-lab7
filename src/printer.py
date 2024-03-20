import os
import pandas as pd

pd.set_option('display.max_columns', None)
try:
    terminal_width = os.get_terminal_size().columns
    pd.set_option('display.width', terminal_width)
except OSError:
    pass

def welcome():
    try:
        terminal_height = os.get_terminal_size().lines - 2
    except OSError:
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
        f"FR5: {f['u']}Rev{f['r']}enue\n"
        f"{f['u']}Q{f['r']}uit\n"
    )
    usr = input(extra + spiel).lower()
    print("\033[H\033[J", end="")
    return usr


def fr1_res(data):
    df = pd.DataFrame(data, columns=["RoomCode", "RoomName", "Beds", "BedType", "MaxOcc", "BasePrice", "Decor", "PopularityScore", "NextAvailableCheckIn", "LengthOfStay", "CheckoutDate"])
    df.index += 1
    print(df)

def fr2_req():
    disp = [
        "First name: ",
        "Last name: ",
        "Room code (“Any” to indicate no preference): ",
        "Bed type (“Any” to indicate no preference): ",
        "Begin date of stay: ",
        "End date of stay: ",
        "Number of children: ",
        "Number of adults: "
    ]
    print(
        "Please enter the following information to make a reservation:\n",
        "\n".join(disp),
        sep="\n"
    )
    options = ["first", "last", "room", "bed", "start", "end", "children", "adults"]
    choices = {}
    for i, option in enumerate(options):
        choices[option] = input(f"\033[0m{disp[i]}\033[4m") if i > 0 else input("\033[3;13H\033[4m")
    print("\033[0m", end="")
    print(choices)
    return choices