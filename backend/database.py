import mysql.connector

from config import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

db = mysql.connector.connect(
    host=DB_HOST,
    port=DB_PORT,
    user=DB_USER,
    password=DB_PASSWORD,
    database=DB_NAME,
    autocommit=True,
)

print("MySQL connection successful!")
