import os
import mysql.connector

def get_db():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
        port=int(os.environ.get("DB_PORT", 3306))
    )

def init_tables():
    db = get_db()
    cur = db.cursor()

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

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT,
        product_id INT,
        quantity INT DEFAULT 1,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
    )
    """)

    db.commit()
    cur.close()
    db.close()
