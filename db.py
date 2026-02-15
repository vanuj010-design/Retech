import os
import mysql.connector
from urllib.parse import urlparse

def get_db():
    url = os.environ.get("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL not set")

    parsed = urlparse(url)

    return mysql.connector.connect(
        host=parsed.hostname,
        user=parsed.username,
        password=parsed.password,
        database=parsed.path.lstrip("/"),
        port=parsed.port,
        autocommit=True
    )

def init_tables():

    db=get_db()
    cur=db.cursor()

    cur.execute("""create table if not exist users (id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(15),
        gender VARCHAR(10),
        age INT,
        email VARCHAR(100) UNIQUE,
        password VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""");

    cur.execute("""create table if not exist products(id INT AUTO_INCREMENT PRIMARY KEY,
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
        image_url VARCHAR(255))""");



    cur.execute("""create table if not exist addresses(id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,

        full_name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        address_line TEXT NOT NULL,
        city VARCHAR(50) NOT NULL,
        state VARCHAR(50) NOT NULL,
        pincode VARCHAR(10) NOT NULL,

        is_default TINYINT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE)""");

    cur.execute("""create table if not exist cart(id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT DEFAULT 1,
        added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE)""");


    cur.execute("""create table if not exist orders(id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        address_id INT NOT NULL,
        total_amount DECIMAL(10,2),
        status VARCHAR(30) DEFAULT 'Placed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (user_id) REFERENCES users(id),
        FOREIGN KEY (address_id) REFERENCES addresses(id))""");


    cur.execute("""create table if not exist order_items(id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        product_id INT NOT NULL,
        quantity INT NOT NULL,
        price DECIMAL(10,2) NOT NULL,

        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
        FOREIGN KEY (product_id) REFERENCES products(id))""");

    cur.execute("""create table if not exist admins(id INT AUTO_INCREMENT PRIMARY KEY,
        admin_id VARCHAR(100) UNIQUE,
        password VARCHAR(255))""");

    cur.execute("""create table if not exist order_status_history(id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        status VARCHAR(30) NOT NULL,
        changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE)""");

    cur.execute("""Create table if not exist( id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        payment_method VARCHAR(30),
        payment_status VARCHAR(30),
        transaction_id VARCHAR(100),
        amount DECIMAL(10,2),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE)""");

    cur.execute("""create table if not exist admin_logs(id INT AUTO_INCREMENT PRIMARY KEY,
        admin_id INT,
        action VARCHAR(255),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY (admin_id) REFERENCES admins(id))""");

    cur.execute("""create table if not exist order_cancellations( id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT NOT NULL,
        user_id INT NOT NULL,
        reason VARCHAR(255) NOT NULL,
        cancelled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        CONSTRAINT fk_cancel_order
            FOREIGN KEY (order_id)
            REFERENCES orders(id)
            ON DELETE CASCADE,

        CONSTRAINT fk_cancel_user
            FOREIGN KEY (user_id)
            REFERENCES users(id)
            ON DELETE CASCADE)""");

    db.commit()
    cur.close()
    db.close()

    print("Table created Successfully")