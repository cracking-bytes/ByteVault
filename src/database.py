import mysql.connector as msc
from mysql.connector import Error

def connect_db():
    try:
        con = msc.connect(
            host = "localhost",
            user = "root",
            password = "genius83"
            )

        if con.is_connected():
            print(" + Connected to MySQL server")

            cursor = con.cursor()
            cursor.execute("CREATE DATABASE IF NOT EXISTS bytevault;")
            print(" + Database 'bytevault' ok")

            cursor.close()
            con.close()

        con = msc.connect(
            host = "localhost",
            user = "root",
            password = "genius83",
            database = "bytevault"
        )

        return con
    
    except Error as e:
        print("Database connection error: ", e)
        return None
    

def setup_table(con):
    try:
        cursor = con.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS vault (
            id INT AUTO_INCREMENT PRIMARY KEY,
            service VARCHAR(100) NOT NULL,
            username VARCHAR(100) NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ); """

        cursor.execute(query)
        con.commit()
        cursor.close()
        print(" + Table 'vault' ok")

    except Error as e:
        print("Table creation error: ", e)


if __name__ == "__main__":
    conn = connect_db()
    if conn:
        setup_table(conn)
        conn.close()
        print(" + Database setup complete")