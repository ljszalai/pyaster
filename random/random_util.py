import string
import random
import time
import uuid
from datetime import datetime

digs = string.digits + string.ascii_letters
DATE_2013_01_01 = 1356998400000
random.seed()


def convert_to_radix(x, base):
    # based on https://stackoverflow.com/a/2267446
    if x < 0:
        sign = -1
    elif x == 0:
        return digs[0]
    else:
        sign = 1

    x *= sign
    digits = []

    while x:
        digits.append(digs[int(x % base)])
        x = int(x / base)

    if sign < 0:
        digits.append('-')

    digits.reverse()

    return ''.join(digits).upper()


def generate_token():
    result = generate_uuid() + generate_id()
    return result[0:47]


def generate_uuid():
    return str(uuid.uuid4())


def generate_id():
    x_ind1 = random.randint(0, 1296)
    x_ind2 = random.randint(0, 1296)
    x_date1 = datetime.now()
    x_date = round(x_date1.timestamp() * 1000) - DATE_2013_01_01
    x_res = convert_to_radix(x_date, 36).ljust(8, '0')
    x_nano = convert_to_radix(time.time_ns(), 36)
    result = x_res + \
             x_nano[-4:] + \
             convert_to_radix(x_ind1, 36).ljust(2, '0') + \
             convert_to_radix(x_ind2, 36).ljust(2, '0')
    return result
