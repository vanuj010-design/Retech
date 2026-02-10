import os
import mysql.connector

def get_db():
    print("DB_HOST =", os.environ.get("DB_HOST"))
    print("DB_USER =", os.environ.get("DB_USER"))
    print("DB_NAME =", os.environ.get("DB_NAME"))

    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=3306
    )
