import random
import string


def create_uid():
    characters = string.ascii_letters + string.digits
    uid = ''.join(random.choice(characters) for _ in range(8))
    return uid


def create_token():
    characters = string.ascii_letters + string.digits
    token = ''.join(random.choice(characters) for _ in range(24))
    return token
