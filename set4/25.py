from common import AES_ECB_decrypt, AES_CTR, randstr
from random import randint


def get_data():
    with open('data/25.txt', 'r') as f:
        data = f.read().decode('base64')
    key = "YELLOW SUBMARINE"
    return AES_ECB_decrypt(data, key)

KEY, NONCE = randstr(16), randint(0, 1 << 64 - 1)
print "[+] Using KEY, NONCE = %s, 0x%x" % (repr(KEY), NONCE)
ciphertext = AES_CTR(get_data(), KEY, NONCE)


def edit_api(offset, newtext):  # ciphertext, key are taken from
                                # global variables, and ciphertext is
                                # edited directly
    global ciphertext
    assert(offset >= 0)
    assert(offset + len(newtext) <= len(ciphertext))
    dec = AES_CTR(ciphertext, KEY, NONCE)
    mod = dec[:offset] + newtext + dec[offset + len(newtext):]
    ciphertext = AES_CTR(mod, KEY, NONCE)


def break_ctr(edit):
    from common import xor_str
    enc = ciphertext[:]
    edit(0, '\x00' * len(enc))
    keystream = ciphertext[:]
    dec = xor_str(enc, keystream)
    edit(0, dec)                # Fix the original ciphertext, so that
                                # no malicious work is seen. Keep your
                                # actions hidden :)
    return dec

plaintext = break_ctr(edit_api)
print "[+] Broke it"
print
print plaintext
