def randstr(n):
    from random import randint
    return ''.join(chr(randint(0, 255)) for _ in range(n))


def pad(data, blocksize=16):
    l = (len(data) / blocksize + 1) * blocksize
    m = l - len(data)
    return data + chr(m) * m


def unpad(data, blocksize=16):
    if len(data) % blocksize != 0:
        raise Exception
    must_unpad = ord(data[-1])
    if must_unpad < 0 or must_unpad > blocksize:
        raise Exception
    if data[-must_unpad:] != chr(must_unpad) * must_unpad:
        raise Exception
    return data[:-must_unpad]


def AES_ECB_encrypt(data, key):
    assert(len(key) == 16)
    assert(len(data) % 16 == 0)
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)


def AES_ECB_decrypt(data, key):
    assert(len(key) == 16)
    assert(len(data) % 16 == 0)
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)


def xor_str(x, y):
    return ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(x, y))


def AES_CBC_encrypt(data, key, iv):
    assert(len(key) == 16)
    assert(len(iv) == 16)
    assert(len(data) % 16 == 0)

    ret = ''
    left = iv
    for i in range(0, len(data), 16):
        right = data[i: i + 16]
        left = AES_ECB_encrypt(xor_str(left, right), key)
        ret += left
    return ret


def AES_CBC_decrypt(data, key, iv):
    assert(len(key) == 16)
    assert(len(iv) == 16)
    assert(len(data) % 16 == 0)

    ret = ''
    left = iv
    for i in range(0, len(data), 16):
        ret += xor_str(left, AES_ECB_decrypt(data[i: i + 16], key))
        left = data[i: i + 16]
    return ret


if __name__ == '__main__':
    assert(pad("YELLOW SUBMARINE", 20) == "YELLOW SUBMARINE\x04\x04\x04\x04")
    assert(unpad("YELLOW SUBMARINE\x04\x04\x04\x04", 20) == "YELLOW SUBMARINE")
    assert(
        AES_ECB_decrypt(
            AES_ECB_encrypt('this is sparta!!',
                            'yellow submarine'),
            'yellow submarine') == 'this is sparta!!')
    assert(
        AES_CBC_decrypt(
            AES_CBC_encrypt(pad('SPACey'),
                            'yellow submarine', '\x00' * 16),
            'yellow submarine', '\x00' * 16) == pad('SPACey', 16))
    print "All tests pass"
