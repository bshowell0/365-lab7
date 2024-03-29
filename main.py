from dotenv import load_dotenv
import os
import mysql.connector
from src import *

load_dotenv()

def main():
    conn = mysql.connector.connect(user=os.getenv('DB_USER'),
                                   password=os.getenv('DB_PASSWORD'),
                                   host=os.getenv('DB_HOST'),
                                   database=os.getenv('DB_NAME'))
    cursor = conn.cursor()
    printer.welcome()
    usr = printer.usr()
    while not validate.quit(usr):
        if validate.fr1(usr):
            request.fr1(cursor)
        elif validate.fr2(usr):
            request.fr2(cursor, conn)
        elif validate.fr3(usr):
            request.fr3(cursor, conn)
        elif validate.fr4(usr):
            request.fr4(cursor)
        elif validate.fr5(usr):
            request.fr5(cursor)
        else:
            printer.invalid()
        usr = printer.usr("\n")

    cursor.close()
    conn.close()


if __name__ == "__main__":
    main()
