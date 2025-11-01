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
        

# ---------- pass manager feaatures

def addp():
    site = input("Site/App name: ")
    user = input("Username: ")
    pw = input("Password: ")
    cur.excute(r"INSERT INTO passwords (site, username, password) VALUES (%s, %s, %s)",
               (site, user, lock(pw)))
    con.commit()
    print(" + Password added successfully")

def viewp():
    cur.execute("SELECT id, site, username, password FROM passwords")
    rows = cur.fetchall()
    for r in rows:
        print(f"\nID: {r[0]} \nSite: {r[1]} \nUser: {r[2]} \nPassword: {unlock(r[3])}")

def updp():
    id_ = input('Enter ID to update: ')
    npw = input("New Password: ")
    cur.execute(r"UPDATE passwords WHERE id=%s", (lock(npw), id_))
    con.commit()
    print("+ Password updated")

def delp():
    id_ = input("Enter ID to delete: ")
    cur.execute(r"DELETE FROM passwords WHERE id=%s", (id_,))
    con.commit()
    print(" + Password deleted")


# ---------- menu

def main():
    if not chkmpw():
        return
    
    while True:
        print(r'''
______         _           _   _                _  _   
| ___ \       | |         | | | |              | || |  
| |_/ / _   _ | |_   ___  | | | |  __ _  _   _ | || |_ 
| ___ \| | | || __| / _ \ | | | | / _` || | | || || __|
| |_/ /| |_| || |_ |  __/ \ \_/ /| (_| || |_| || || |_ 
\____/  \__, | \__| \___|  \___/  \__,_| \__,_||_| \__|
         __/ |                                       
        |___/                                                                     
''')
        print('''
1. Add Password
2. View Password
3. Update Password
4. Delete Password
5. Exit
''')
        
        ch = input("Enter your choice: ")

        if ch == '1':
            addp()
        elif ch == '2':
            viewp()
        elif ch == '3':
            updp()
        elif ch == '4':
            delp()
        elif ch == '5':
            print("Exiting ByteVault...")
            break
        else:
            print("Invalid choice. Try again!")

if __name__ == "__main__":
    main()
    con.close()       
