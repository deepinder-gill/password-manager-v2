import base64
import os
import json
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import re 

def derive_key(master_pass, salt):
  kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),
    length = 32,
    salt = salt,
    iterations=100_000
  )
  return base64.urlsafe_b64encode(kdf.derive(master_pass.encode()))

def master_password():
    if os.path.exists("salt.bin"):
      master_pass = input("ENTER PASSWORD:")
      with open("salt.bin", "rb") as salt_file:
        salt = salt_file.read()
      key = derive_key(master_pass, salt)
      master_key = Fernet(key)

      with open("check.bin", "rb") as check_authentication:
        to_verify = check_authentication.read()
      try:
        check = master_key.decrypt(to_verify)
        return master_key
      except InvalidToken:
        print("ACCESS DENIED! WRONG PASSWORD")
        return None 
      

    else:
      setup_pass = input("PLEASE SET'up A MASTER KEY FOR THIS PROGRAM")
      salt = os.urandom(16)
      with open("salt.bin", "wb") as salt_file:
        salt_file.write(salt)
      key = derive_key(setup_pass, salt)
      master_key = Fernet(key)

      check = master_key.encrypt(b"authentication checked")
      with open("check.bin", "wb") as check_authentication:
        check_authentication.write(check)
      return master_key

def ask_user():
  while True:
    try:
      ask = int(input("1. Add password\n2. View passwords\n3. Search password\n4. Delete password\n5. Exit\nPlease enter what you wish to do(1-5): "))
      if ask in (1, 2, 3, 4, 5):
        return ask
      else:
        print("please enter betweeen 1-6!")

    except ValueError:
      print("INVALID VALUE! only integers allowed and they must be in 1-6")

def s_name():
  while True:
   # pattern = '^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}(\/[^\s]*)?$'
    name = input("ENTER SERVICE's URL: ").strip()
   # if re.match(pattern, name):
    return name
  
def u_name():
  while True:
    name = input("ENTER USERNAME: ").strip()
    if len(name) >= 1:
      return name
    else:
      print("USERNAME can't be empty!")

def p_word(vault_key):
  while True:
    password = input("ENTER PASSWORD: ")
    if len(password) >= 1:
      encrypted_password = vault_key.encrypt(password.encode())
      return encrypted_password.decode()
    else:
      print("PASSWORD can't be empty!")
  
def add_password(vault_key):
  if os.path.exists("data.json"):
    service_name = s_name()
    username = u_name()
    password = p_word(vault_key)
    new_data = { "SERVICE" : service_name, "USERNAME" : username, "PASSWORD" : password}
    old_data = []
    with open("data.json", "r") as previous_data:
      read_data = json.load(previous_data)

    read_data.append(new_data)
    with open("data.json", "w") as to_upload:
      json.dump(read_data, to_upload, indent = 4)
    
  else:
    service_name = s_name()
    username = u_name()
    password = p_word(vault_key)

    data= []
    new_data = { "SERVICE" : service_name, "USERNAME" : username, "PASSWORD" : password}
    data.append(new_data)

    with open("data.json", "w") as to_upload:
      json.dump(data, to_upload, indent = 4)

def view_password(vault_key):
  if os.path.exists("data.json"):
    entries = []
    with open("data.json", "r") as file:
      entries = json.load(file)

      for line in entries:
        print(f" SERVICE NAME: {line['SERVICE']}")
        print(f"USERNAME: {line['USERNAME']}")
        print(f"PASSWORD: {vault_key.decrypt(line['PASSWORD'].encode()).decode()}")

  else:
    print("NO PASSWORDS STORED YET!!")

def search_password(vault_key):
  while True:
    name = input("ENTER URL: ")
    entries = []

    with open("data.json", "r") as read_data:
      entries = json.load(read_data)

    for  i, line in enumerate(entries) :
      if name == line["SERVICE"]:

         print(f" SERVICE NAME: {line['SERVICE']}")
         print(f"USERNAME: {line['USERNAME']}")
         print(f"PASSWORD: {vault_key.decrypt(line['PASSWORD'].encode()).decode()}")
         return

    else:
      print("INVALID SERVICE!")
      return
    
def delete_password(vault_key):
  if not os.path.exists("data.json"):
    print("STORE SOME PASSWORDS FIRST")
    return

  to_delete = input("Enter Service you wish to delete: ")
  if not to_delete:
      print("SERVCE NAME CANT BE EMPTY")

  else:
    with open("data.json", "r") as file:
      read_file = json.load(file)
      for i, line in enumerate(read_file):
        try:
          if to_delete == line["SERVICE"]:
            read_file.pop(i)
            with open("data.json", "w") as new_data:
              json.dump(read_file, new_data, indent = 4)
              break
        except:
          print("THIS SERVICE DOESN't EXIST IN DATA!!")
          break

def exit_program():
  while True:
    if_exit = input("DO YOU WISH TO EXIT THE PROGRAM? [y/n]").lower().strip()
    if if_exit in ("y", "n"):
      return if_exit
    else: 
      print("PLEASE ENTER VALID VALUE!!!")

def more():
  while True:
    _more = input("Do you wish to do more?[y/n]").lower().strip()
    if _more in ("y", "n"):
      return _more
    else:
      print("INVALID VALUE PLEASE CHOOSE BETWEEN [y/n]")

def main() :
  vault_key = master_password()
  if not vault_key:
    return None
  
  while True:
    user_decision = ask_user()
    if user_decision == 1 :
      add_password(vault_key)
      again = more()
      if again == "n":
        print("THANKYOU, FOR USING OUR SERVICE!")
        break 
    elif user_decision == 2 :
      view_password(vault_key)
      again = more()
      if again == "n":
        print("THANKYOU, FOR USING OUR SERVICE!")
        break 
    elif user_decision == 3 :
      search_password(vault_key)
      again = more()
      if again == "n":
        print("THANKYOU, FOR USING OUR SERVICE!")
        break  
    elif user_decision  == 4:
      delete_password(vault_key)
      again = more()
      if again == "n":
        print("THANKYOU, FOR USING OUR SERVICE!")
        break 
    elif user_decision == 5:
      _exit = exit_program()
      if _exit == "y":
        break

if __name__ == "__main__":
  main()   
  