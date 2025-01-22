import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

def get_access_key():
    return ACCESS_KEY

def get_secret_key():
    return SECRET_KEY
