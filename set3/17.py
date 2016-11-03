from common import randstr, AES_CBC_encrypt, AES_CBC_decrypt, \
    pad, unpad, xor_str
from random import choice

oracle_key = randstr(16)


def encryption_oracle():
    data = (
        """
        MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=
        MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=
        MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==
        MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==
        MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl
        MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==
        MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==
        MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=
        MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=
        MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93
        """).split()
    iv = randstr(16)
    data = choice(data).decode('base64')
    return (iv, AES_CBC_encrypt(pad(data), oracle_key, iv))


def padding_oracle(iv, data):
    dec = AES_CBC_decrypt(data, oracle_key, iv)
    try:
        unpad(dec)
        return True
    except:
        return False


# And the actual attack now...


def crack_block(padding_oracle, iv, block):
    assert(len(iv) == 16)
    assert(len(block) == 16)

    def do_pad(iv, suffix):
        l = len(suffix)
        t = 'x' * (16 - l)
        r = xor_str(xor_str(t + chr(l) * l, t + suffix), iv)
        return r

    rev = ''
    if padding_oracle(iv, block):  # Pre-padded block
        for i in range(16):
            a = 'x'*i + '\xff' + 'x'*(16 - i - 1)
            b = 'x'*i + '\x00' + 'x'*(16 - i - 1)
            test_iv = xor_str(xor_str(a, b), iv)
            if not padding_oracle(test_iv, block):
                rev = chr(16 - i) * (16 - i)
                break

    for i in range(16 - len(rev)):
        for j in range(256):
            guess = (rev + chr(j))[::-1]
            new_iv = do_pad(iv, guess)
            # print repr(iv), repr(new_iv), repr(block)
            if padding_oracle(new_iv, block):
                rev += chr(j)
                break
    return rev[::-1]


def padding_attack(padding_oracle, iv, ciphertext):
    ret = ''
    prev = iv
    for i in range(0, len(ciphertext), 16):
        cracked = crack_block(padding_oracle, prev, ciphertext[i: i+16])
        ret += cracked
        prev = ciphertext[i:i+16]
    return unpad(ret)


def main():
    answers = []
    while len(answers) < 10:    # We know this somehow
        iv, c = encryption_oracle()
        dec = padding_attack(padding_oracle, iv, c)
        if dec not in answers:
            answers.append(dec)
            answers.sort()
            print '\n'.join(repr(a) for a in answers)
            print


if __name__ == '__main__':
    main()
