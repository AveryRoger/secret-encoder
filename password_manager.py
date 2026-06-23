### 
# To whomever is reading this I am sorry in advance for my spaghetti
# READ ME
# if EITHER data file is missing OR empty this will wipe everything in there
# IF you enter the wrong master password and chose to EDIT it will decrypte garbage and you will overwritten with garbage
# THIS DOES NOT VERIFY PASSWORDS use at your own risk
# PLEASE DO NOT STORE IMPORTANT INFO UNLESS YOU KNOW THE RISKS
# also ASCII is used for the characters so no emojis or anything crazy or else it breaks K.I.S.S keep, it , simple, stupid
# feel free to take this edit it and repost to github your better versions!!!
###

# im importing things to be used later
import os
import secrets
import getpass
import hashlib
import json

# this is the main loop so i can run continosuly and break off and stuff YOU MAY NEED TO EDIT FILE_PATH AND KEY_FILE
while True:
    
    base = os.path.expanduser("~/password_manager")
    file_path = os.path.join(base, "password_manager.txt")
    key_file = os.path.join(base, "key_data.txt")


# above im defining these values like the mode and file path and stuff will be made if you dont have one later

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    #checking if a file path exists or are empty
    if (not os.path.exists(file_path) or os.path.getsize(file_path) == 0 or
        not os.path.exists(key_file) or os.path.getsize(key_file) == 0):
            #if no file path exists this will run or if its empty
            print("initializing")
            converted = []
            key = []
            encoded = []
            salt = secrets.token_bytes(16)
            #im asking for stuff here
            password = getpass.getpass("create master password:")
            starting_phrase = input("input what you want in your password manager")
            
            #its encoding what you wrote down here for the size and stuff
            for letters in starting_phrase:
                converted.append(ord(letters))
            for num in converted:
                r = secrets.randbelow(256)
                key.append(r)
                new_num = num ^ r
                encoded.append(new_num)
            
            password_key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt,
            100000,
            dklen=len(key)
        )
            # making your encrypted key and the data which goes with it
            encrypted_key = []
            for i in range(len(key)):
                k = password_key[i]
                new_value = key[i] ^ k
                encrypted_key.append(new_value)
            
            data = {
                "salt": list(salt),
                "encrypted_key": encrypted_key
            }
            #literally makes the file path for you and forces you to restart and run again so no initialisation
            with open(file_path, "w") as f:
                json.dump(encoded, f)
            with open(key_file, "w") as f:
                json.dump(data, f)
            print("setup complete restart program")
            exit()

#this is start of the main code what youll use most times
    start = input("do you want to open password manager?(y/n):").lower()
    #Main Code after asking if you want to open
    if start == "y":
        # this open the file paths previously created and reads them
        try:
            with open(file_path, "r") as f:
                encoded = json.loads(f.read())
        
            with open(key_file, "r") as f:
                data = json.loads(f.read())
        except Exception as e:
            print("ERROR: Could not read or parse your password files.")
            print("Reason:", e)
            print("Your files may be corrupted or partially written.")
            continue
        salt = bytes(data["salt"])
        encrypted_key = data["encrypted_key"]
       ### it gets values from those files above and asks for the password
       # the password is the main security in this so please make a good one
       # if you forget you password, too bad so sad everything will be wiped if you EDIT
       # SO IF YOU ARE UNSURE YOU PASSWORD DO NOT EDIT!!! ONLY READ###
        password = getpass.getpass("enter master password:")
        # THIS IS A NO IF UNSURE PASSWORD
        edit_file = input("do you want to edit passwords?(y/n):").lower()

        #editing the file section if NO
        if edit_file == "n":
            #decoding the text ->
            #hashing the password
            password_key =  hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt,
                100000,
                dklen=len(encrypted_key)
                )
            key = []
            #making your key
            for i in range(len(encrypted_key)):
                k = password_key[i]
                key.append(encrypted_key[i] ^  k)
            if len(encoded) != len(key):
                    print("key and message length do not match")
                    continue
            decoded = []
        # then putting it all together and decoding it and putting this into decoded list
            for i in range(len(encoded)):
                original = encoded[i] ^ key[i]
                letter = chr(original)
                decoded.append(letter)
            
            decoded_text = "".join(decoded)
            print(decoded_text)
            #end of decoding text <-
            close = input("do you want to close password manager?(y/n)").lower()
            # rencrypteds and saves
            salt = secrets.token_bytes(16)
            converted = []
            encoded = []
            key = []
            phrase = decoded_text
            #takes phrase and puts it into converted
            for letters in phrase:
                converted.append(ord(letters))
            # for every number in converted apply the logic below
            for num in converted:
                r = secrets.randbelow(256)
                key.append(r)
                new_num = num ^ r
                encoded.append(new_num)
            password_key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt,
                100000,
                dklen=len(key)
            )
            # now makes your encrypted key by putting all together
            encrypted_key = []
            for i in range(len(key)):
                k = password_key[i]
                new_value = key[i] ^ k
                encrypted_key.append(new_value)
            data = {"salt": list(salt),
            "encrypted_key": encrypted_key
            }
            #opens your files and rewrites password_manager and key_data
            try:
                with open(file_path, "w") as f:
                    json.dump(encoded, f)
                with open(key_file, "w") as f:
                    json.dump(data, f)
            except Exception as e:
                print("ERROR: Failed to save your encrypted data.")
                print("Reason:", e)
                print("Your vault may not have been updated.")
                continue
            # if you want to close it closes else it continues
            if close == "y":
                exit()
            else:
                continue
        # if you do want to edit file MUST BE SURE OF PASSWORD OR IT WILL DECRYPTE GARBAGE
        elif edit_file == "y":
            #taking master password and applying it
            password_key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt,
                100000,
                dklen=len(encrypted_key)
            )
            # decrypting your encrypted key
            key = []
            for i in range(len(encrypted_key)):
                k = password_key[i]
                key.append(encrypted_key[i] ^ k)
            # decryptes the full thing now
            decoded = []
            for i in range(len(encoded)):
                original = encoded[i] ^ key[i]
                decoded.append(chr(original))
            # this is now printing your currently stored text in decoded
            decoded_text = "".join(decoded)
            print("\nCurrent stored text:")
            print(decoded_text)
            #encrypting what you wrote
            print("\nEnter your NEW password manager contents:")
            new_text = input("> ")

            # re-encrypt
            salt = secrets.token_bytes(16)
            converted = [ord(c) for c in new_text]
            key = [secrets.randbelow(256) for _ in converted]
            encoded = [converted[i] ^ key[i] for i in range(len(converted))]
            # password application to your key is being made here
            password_key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode(),
                salt,
                100000,
                dklen=len(key)
            )
            # this is your full encrypted key
            encrypted_key = [key[i] ^ password_key[i] for i in range(len(key))]
            # this is what goes into the file
            data = {
                "salt": list(salt),
                "encrypted_key": encrypted_key
            }
            # writing in said files your encoded text and key
            try:
                with open(file_path, "w") as f:
                    json.dump(encoded, f)
                with open(key_file, "w") as f:
                    json.dump(data, f)
            except Exception as e:
                print("ERROR: Failed to save your encrypted data.")
                print("Reason:", e)
                print("Your vault may not have been updated.")
                continue
            print("Updated and saved.")
    elif start == "n":
        exit()
    else:
        print("what? its y or n bruv")
        continue