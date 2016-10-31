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


def hamming(x, y):
    assert(len(x) == len(y))

    def popcount(a):
        if a == 0:
            return 0
        else:
            return (a % 2) + popcount(a / 2)

    return sum(popcount(ord(a) ^ ord(b)) for a, b in zip(x, y))


def AES_ECB_encrypt(data, key):
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(data)


def AES_ECB_decrypt(data, key):
    from Crypto.Cipher import AES
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.decrypt(data)

if __name__ == '__main__':
    # Testing!
    assert(score('this is sparta!') == 12702)  # I know, not a very nice test, but meh... :P
    assert(hamming('this is a test', 'wokka wokka!!!') == 37)
    assert(
        AES_ECB_decrypt(
            AES_ECB_encrypt('this is sparta!!',
                            'yellow submarine'),
            'yellow submarine') == 'this is sparta!!')
    print "All tests pass"
