import os
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("mysql.railway.internal"),
        user=os.environ.get("root"),
        password=os.environ.get("KzrPQbswqyGVXGGVuTumDKCQidBSRyFd"),
        database=os.environ.get("railway")
    )
