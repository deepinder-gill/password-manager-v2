import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def master_password():
  master_pass = input("ENTER THE KEY TO THE VAULT")

  salt = os.urandom(16)

  key = derive_key(master_pass, salt)



def main() :
  master_password()