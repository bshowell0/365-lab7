from dotenv import load_dotenv
import os
import mysql.connector
from src import *

load_dotenv()
try:
    terminal_height = os.get_terminal_size().lines - 1
except:
    terminal_height = 100

def main():
    f = {"u": "\033[4m", "r": "\033[0m"}  # format: [underline, reset]
    spiel = (
        "Please select an option:\n\n"
        f"FR1: {f['u']}Rooms{f['r']} and {f['u']}Rates{f['r']}\n"
        f"FR2: {f['u']}Res{f['r']}ervations\n"
        f"FR3: Reservation {f['u']}Cancel{f['r']}lation\n"
        f"FR4: {f['u']}Detail{f['r']}ed Reservation {f['u']}Info{f['r']}rmation\n"
        f"{f['u']}Q{f['r']}uit\n"
    )
    print("\n" * terminal_height + "\033[H\033[J", end="")
    print("Welcome to the Hotel Reservation System!")
    usr = input(spiel).lower()
    print("\033[H\033[J", end="")
    while usr != "q" and usr != "quit":
        # do stuff
        if usr == "fr1" or usr == "rooms and rates" or usr == "rooms" or usr == "rates":
            pass
        elif usr == "fr2" or usr == "reservations" or usr == "res":
            pass
        elif usr == "fr3" or usr == "reservation cancellation" or usr == "cancel":
            pass
        elif usr == "fr4" or usr == "detailed reservation information" or usr == "detail" or usr == "info":
            pass
        else:
            print("Invalid input.\nType the code, full name, or underlined portion.\nE.g. 'FR1', 'Rooms and Rates', 'Rooms', or 'Rates'.\nCase insensitive.\n'Q' or 'Quit' to exit.")
        usr = input("\n" + spiel).lower()
        print("\033[H\033[J", end="")



    # conn = mysql.connector.connect(user=os.getenv('DB_USER'),
    #                                password=os.getenv('DB_PASSWORD'),
    #                                host='mysql.labthreesixfive.com',
    #                                database=os.getenv('DB_NAME'))
    # cursor = conn.cursor()

    # conn.commit()

    # cursor.close()
    # conn.close()


if __name__ == "__main__":
    main()
