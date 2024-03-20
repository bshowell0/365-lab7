from dotenv import load_dotenv
import os
import mysql.connector
from src import *

load_dotenv()

# add `# type: ignore` to supress incorrect not defined errors

def main():
    conn = mysql.connector.connect(user=os.getenv('DB_USER'),
                                   password=os.getenv('DB_PASSWORD'),
                                   host='mysql.labthreesixfive.com',
                                   database=os.getenv('DB_NAME'))
    cursor = conn.cursor()
    pprint.welcome()
    usr = pprint.usr()
    while not validate.quit(usr):
        if validate.fr1(usr):
            pass
        elif validate.fr2(usr):
            pass
        elif validate.fr3(usr):
            pass
        elif validate.fr4(usr):
            pass
        else:
            pprint.invalid()
        usr = pprint.usr("\n")




    # conn.commit()

    # cursor.close()
    # conn.close()


if __name__ == "__main__":
    main()
