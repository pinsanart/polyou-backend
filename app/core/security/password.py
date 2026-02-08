from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

def verify_password_hash(password: str, hash: str):
    return password_hash.verify(password, hash)

def hash_password(password: str):
    return password_hash.hash(password)