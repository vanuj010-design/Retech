import os
import mysql.connector
from mysql.connector import pooling

# ---------- CONNECTION POOL (RENDER SAFE) ----------
dbconfig = {
    "host": os.environ.get("MYSQLHOST"),
    "port": int(os.environ.get("MYSQLPORT", 3306)),
    "user": os.environ.get("MYSQLUSER"),
    "password": os.environ.get("MYSQLPASSWORD"),
    "database": os.environ.get("MYSQLDATABASE"),
}

# Validate env vars early (helps debugging on Render)
missing = [k for k, v in dbconfig.items() if v is None]
if missing:
    raise RuntimeError(f"MySQL ENV vars missing: {missing}")

pool = pooling.MySQLConnectionPool(
    pool_name="retech_pool",
    pool_size=5,
    **dbconfig
)

# ---------- GET DB ----------
def get_db():
    return pool.get_connection()

# ---------- INIT TABLES (SAFE TO CALL) ----------
def init_tables():
    db = get_db()
    cur = db.cursor()

    # Example minimal safety table (your real tables already exist)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            admin_id VARCHAR(100) UNIQUE,
            password VARCHAR(255)
        )
    """)

    db.commit()
    cur.close()
    db.close()
