from common import AES_CTR, randstr, score, xor_str
from random import randint
from itertools import cycle


def get_enc():
    with open('data/20.txt', 'r') as f:
        data = f.read().split()

    data = [a.decode('base64') for a in data]

    key = randstr(16)
    nonce = randint(0, 2**64 - 1)

    enc = [AES_CTR(a, key, nonce) for a in data]

    return enc


def solve(enc):
    mlen = min(len(a) for a in enc)
    enc = [a[:mlen] for a in enc]

    key = ''
    for i in range(mlen):
        e = ''.join(a[i] for a in enc)
        scorer = lambda k: score(xor_str(e, cycle(chr(k))))
        scores = [scorer(k) for k in range(256)]
        key += chr(max(range(256), key=lambda k: scores[k]))

    return key


enc = get_enc()
key = solve(enc)
print "Effective Key:", repr(key)

print "Decryptions:", [xor_str(e, key) for e in enc]
