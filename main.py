from dotenv import load_dotenv
import os
import mysql.connector
from src import *

load_dotenv()


def main():
    pprint.welcome()  # type: ignore
    usr = pprint.usr()  # type: ignore
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
            pprint.invalid()  # type: ignore
        usr = pprint.usr("\n")  # type: ignore



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
