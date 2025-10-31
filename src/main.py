from cryptography.fernet import Fernet as fn
import os

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

print("key path: ", kpath)
print("exist: ", os.path.exists(kpath))

if not os.path.exists(kpath):
    genkey()

key = loadk()
fernet = fn(key)
print(" + Ecryption key loaded")


def lock(text:str) -> bytes:
    # enc lock (plaintext) to ciphertext

    data = text.encode()
    token = fernet.encrypt(data)
    print(" + Password encrypted")
    
    return token

def unlock(token:bytes) -> str:
    # dec unlock ciphertext back to readable

    try:
        data = fernet.decrypt(token)
        plain = data.decode()
        print(" + password decrypted")

        return plain
    
    except Exception as e:
        print("Decryption failed :( ", e)
        return None
    

if __name__ == "__main__":
    sample = "MyPassword123"
    token = lock(sample)
    print("Encrypted: ", token)
    print("Decrypted: ", unlock(token))