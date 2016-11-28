def score(string):
    freq = dict()
    freq['a'] = 834
    freq['b'] = 154
    freq['c'] = 273
    freq['d'] = 414
    freq['e'] = 1260
    freq['f'] = 203
    freq['g'] = 192
    freq['h'] = 611
    freq['i'] = 671
    freq['j'] = 23
    freq['k'] = 87
    freq['l'] = 424
    freq['m'] = 253
    freq['n'] = 680
    freq['o'] = 770
    freq['p'] = 166
    freq['q'] = 9
    freq['r'] = 568
    freq['s'] = 611
    freq['t'] = 937
    freq['u'] = 285
    freq['v'] = 106
    freq['w'] = 234
    freq['x'] = 20
    freq['y'] = 204
    freq['z'] = 6
    freq[' '] = 2320

    ret = 0

    for c in string.lower():
        if c in freq:
            ret += freq[c]

    return ret


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


def AES_CTR_keystream_block(key, nonce, block_number):
    from struct import pack
    data1 = pack('<Q', nonce)    # Little-endian, 64 bits
    data2 = pack('<Q', block_number)
    return AES_ECB_encrypt(data1 + data2, key)


def AES_CTR_keystream(key, nonce):
    block_number = 0
    while True:
        ks_block = AES_CTR_keystream_block(key, nonce, block_number)
        for k in ks_block:
            yield k
        block_number += 1


def AES_CTR(data, key, nonce):
    return xor_str(data, AES_CTR_keystream(key, nonce))


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
    assert(
        AES_CTR(
            AES_CTR('Outta spaceeeeee',
                    'YELLOW SUBMARINE', 0),
            'YELLOW SUBMARINE', 0) == 'Outta spaceeeeee')
    print "All tests pass"
