import hashlib
import json

def hash_pass(password:str) -> str:
    password_bytes = password.encode("utf-8")
    hashed = hashlib.sha256(password_bytes).hexdigest()
    return hashed 


def load(username:str,password:str) -> bool:
    with open('users.json','r') as file:
        data = json.load(file)
    if username in data and data[username] == hash_pass(password):
        return True
    return False     
    