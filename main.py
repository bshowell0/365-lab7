from dotenv import load_dotenv
from os import getenv
import mysql.connector

load_dotenv()


def main():
    conn = mysql.connector.connect(user=getenv('DB_USER'),
                                   password=getenv('DB_PASSWORD'),
                                   host='mysql.labthreesixfive.com',
                                   database=getenv('DB_NAME'))

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hp_goods WHERE flavor = 'Chocolate'")
    result = cursor.fetchall()
    print(result)




if __name__ == "__main__":
    main()
