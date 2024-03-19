from dotenv import load_dotenv
from os import getenv
import mysql.connector

load_dotenv()  # take environment variables from .env.


# Code of your application, which uses environment variables (e.g. from `os.environ` or
# `os.getenv`) as if they came from the actual environment.

conn = mysql.connector.connect(user=getenv('DB_USER'), password=getenv('DB_PASSWORD'),
                               host='mysql.labthreesixfive.com',
                               database=getenv('DB_NAME'))

print(conn)

cursor = conn.cursor()
cursor.execute("SELECT * FROM hp_goods WHERE flavor = 'Chocolate'")
result = cursor.fetchall()
print(result)


