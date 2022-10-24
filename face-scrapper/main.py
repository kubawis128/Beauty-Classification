import requests
import shutil
import hashlib
import os
def file_as_bytes(file):
    with file:
        return file.read()

hash_old = 0;
def bierz(i):
    session = requests.session()
    headers = {'user-Agent': 'Mozilla/5.0'}
    url = "https://thispersondoesnotexist.com/"
    r = requests.get("https://thispersondoesnotexist.com/image", stream=True)
    if r.status_code == 200:
        with open("./face/" + str(i) + ".png", 'wb') as f:
            r.raw.decode_content = True
            hash_old = str(hashlib.md5(file_as_bytes(open("./face/" + str(i-1) + ".png", 'rb'))).hexdigest());
            shutil.copyfileobj(r.raw, f)
            if str(hashlib.md5(file_as_bytes(open("./face/" + str(i) + ".png", 'rb'))).hexdigest()) == str(hash_old):
                print("dup!")
                return -1
            else:
                return 1
            
i = 36
pop = 0;
while True:
    i = i + bierz(i) 
