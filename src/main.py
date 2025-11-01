from cryptography.fernet import Fernet as fn
import os
import mysql.connector as msc


# ---------- encryption setup

basedir = os.path.dirname(os.path.abspath(__file__))
kpath = os.path.join(".", "backup", "secret.key")

def genkey():
    # gen a fernet key and saving to secret.key

    os.makedirs(os.path.dirname(kpath), exist_ok=True)
    
    key = fn.generate_key()
    with open(kpath, 'wb') as keyf:
        keyf.write(key)
    
    print(" + New encryption key generated")

def loadk():
    # loading existing fernet keyy from file

    with open(kpath, 'rb') as keyf:
        key = keyf.read()

    return key

# print("key path: ", kpath)
# print("exist: ", os.path.exists(kpath))

if not os.path.exists(kpath):
    genkey()

# key = loadk()
# fernet = fn(key)
# print(" + Ecryption key loaded")

fernet = fn(loadk())


def lock(text:str) -> bytes:   
    return fernet.encrypt(text.encode())

def unlock(token:bytes) -> str:
    return fernet.decrypt(token).decode()


# ---------- mysql connection

def connect_db():
    try:
        con = msc.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "bytevault"
        )

        cur = con.cursor()
        print(" + Connected to MySQL")
        return con, cur
    
    except Exception as e:
        print(" - Database connection failed", e)
        exit()

con, cur = connect_db()


# ---------- master password

def setp():
    pw = input("Set a master password: ")
    cur.execute(r"INSERT INTO master (id, master_pass) VALUES (1, %s)", (lock(pw),))
    con.commit()
    print(" + Master password set successfully")

def chkmpw():
    cur.execute("SELECT master_pass FROM master WHERE id=1")
    result = cur.fetchone()
    if not result:
        setp()
        return True
    else:
        pw = input("Enter master password: ")
        if unlock(result[0]) == pw:
            print(" + Access granted")
            return True
        else:
            print("Access denied")
            return False
        



    

if __name__ == "__main__":
    sample = "MyPassword123"
    token = lock(sample)
    print("Encrypted: ", token)
    print("Decrypted: ", unlock(token))


# ---------- 