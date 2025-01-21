import os
from dotenv import load_dotenv

load_dotenv()

ACCESS_KEY = os.getenv("UPBIT_ACCESS_KEY")
SECRET_KEY = os.getenv("UPBIT_SECRET_KEY")

def getAccessKey():
    return ACCESS_KEY

def getSecretKey():
    return SECRET_KEY
