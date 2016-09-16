#! /usr/bin/python3

from pwd import getpwnam
import string
import re

def filter_username(username):
    username = username.lower()
    username = re.sub('[^' + string.ascii_lowercase + string.digits + ']', '', username)
    username = username.lstrip(string.digits)
    return username

def username_exists(username):
    try:
        getpwnam(username)
        return True
    except KeyError:
        return False

def generate_username(prefix):
    suffix = 0
    while username_exists(prefix + str(suffix)):
        suffix += 1
    return prefix + str(suffix)

def generate_string(length):
    from random import choice
    chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
    return "".join([choice(chars) for _ in range(length)])

def generate_password(length):
    import crypt
    generated_password = generate_string(length)
    salt = crypt.mksalt()
    encrypted = crypt.crypt(generated_password, salt)
    return encrypted

def create_user(username):
    import subprocess
    username = filter_username(username)
    if len(username) == 0:
        print("Could not create a valid username from the given name")
        return False
    generated_username = generate_username(username)
    password = generate_password(8)
    res = subprocess.call(["useradd", "-p", password, "-m", generated_username], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(res)

create_user("asd")
