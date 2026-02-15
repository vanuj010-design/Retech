import os
import mysql.connector
from mysql.connector import pooling

# ---------- CONNECTION POOL ----------
dbconfig = {
    "host": os.environ.get("MYSQLHOST"),
    "port": int(os.environ.get("MYSQLPORT", 3306)),
    "user": os.environ.get("MYSQLUSER"),
    "password": os.environ.get("MYSQLPASSWORD"),
    "database": os.environ.get("MYSQLDATABASE"),
}

missing = [k for k, v in dbconfig.items() if v is None]
if missing:
    raise RuntimeError(f"MySQL ENV vars missing: {missing}")

pool = pooling.MySQLConnectionPool(
    pool_name="retech_pool",
    pool_size=5,
    **dbconfig
)

def get_db():
    return pool.get_connection()


# ---------- CREATE TABLES ----------
def init_tables():
    db = get_db()
    cur = db.cursor()

    # USERS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            phone VARCHAR(15),
            gender VARCHAR(10),
            age INT,
            email VARCHAR(100) UNIQUE,
            password VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # ADMINS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            admin_id VARCHAR(100) UNIQUE,
            password VARCHAR(255)
        )
    """)

    # PRODUCTS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(150),
            brand VARCHAR(50),
            model_number VARCHAR(50),
            price INT,
            ram VARCHAR(20),
            rom VARCHAR(20),
            color VARCHAR(30),
            operating_system VARCHAR(50),
            display_type VARCHAR(50),
            resolution VARCHAR(30),
            refresh_rate VARCHAR(20),
            launch_year INT,
            product_condition VARCHAR(30),
            image_url VARCHAR(255),
            stock INT DEFAULT 0,
            is_active TINYINT DEFAULT 1
        )
    """)

    # ADDRESSES
    cur.execute("""
        CREATE TABLE IF NOT EXISTS addresses (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            full_name VARCHAR(100) NOT NULL,
            phone VARCHAR(20) NOT NULL,
            address_line TEXT NOT NULL,
            city VARCHAR(50) NOT NULL,
            state VARCHAR(50) NOT NULL,
            pincode VARCHAR(10) NOT NULL,
            is_default TINYINT DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    # ORDERS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            address_id INT NOT NULL,
            total_amount DECIMAL(10,2),
            status VARCHAR(30) DEFAULT 'Placed',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (address_id) REFERENCES addresses(id)
        )
    """)

    # CART
    cur.execute("""
        CREATE TABLE IF NOT EXISTS cart (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT DEFAULT 1,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        )
    """)

    # ORDER ITEMS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_items (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            product_id INT NOT NULL,
            quantity INT NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id)
        )
    """)

    # ORDER STATUS HISTORY
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_status_history (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            status VARCHAR(30) NOT NULL,
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
    """)

    # PAYMENTS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            payment_method VARCHAR(30),
            payment_status VARCHAR(30),
            transaction_id VARCHAR(100),
            amount DECIMAL(10,2),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
        )
    """)

    # ADMIN LOGS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS admin_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            admin_id INT,
            action VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (admin_id) REFERENCES admins(id)
        )
    """)

    # ORDER CANCELLATIONS
    cur.execute("""
        CREATE TABLE IF NOT EXISTS order_cancellations (
            id INT AUTO_INCREMENT PRIMARY KEY,
            order_id INT NOT NULL,
            user_id INT NOT NULL,
            reason VARCHAR(255) NOT NULL,
            cancelled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
    """)

    db.commit()
    cur.close()
    db.close()
