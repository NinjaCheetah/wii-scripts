# "tkey-gen" from wii-scripts by NinjaCheetah
# https://github.com/NinjaCheetah/wii-scripts
# Roughly converted from PHP so probably doesn't make the most sense everywhere.

import sys
import hashlib


def secret(start, length):
    ret = b''
    add = start + length
    for _ in range(length):
        unsigned_start = start & 0xFF  # Compensates for how Python handles negative values vs PHP.
        ret += bytes.fromhex(f"{unsigned_start:02x}"[-2:])
        nxt = start + add
        add = start
        start = nxt
    return ret


def mungetid(tid):
    # Remove leading zeroes from the TID.
    while tid.startswith("00"):
        tid = tid[2:]
    if tid == "":
        tid = "00"
    # In PHP, the last character just gets dropped if you make a hex string from an odd-length input, so this
    # replicates that functionality.
    if len(tid) % 2 != 0:
        tid = tid[:-1]
    return bytes.fromhex(tid)


SECRET = secret(-3, 10)
def derive(tid, passwd):
    global SECRET
    salt = hashlib.md5(SECRET + mungetid(tid)).digest()
    # Had to reduce the length here from 32 to 16 when converting to get the same length keys.
    return hashlib.pbkdf2_hmac("sha1", passwd.encode(), salt, 20, 16).hex()


def derive_all(tid):
    # Add new passwords here as needed.
    passes = ["nintendo", "mypass"]
    for passwd in passes:
        print(f"{tid} : {derive(tid, passwd)} [{passwd}]")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: tkey-gen.py <TID>")
        sys.exit(1)
    derive_all(sys.argv[1])
