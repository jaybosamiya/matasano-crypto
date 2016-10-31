from common import hamming, score
from itertools import cycle

with open('data/6.txt', 'r') as f:
    data = f.read().decode('base64')


def xor(enc, k):
    return ''.join(chr(ord(a) ^ k) for a in enc)


def norm_dist(keysize):
    numblocks = (len(data) / keysize)
    blocksum = 0
    for i in range(numblocks - 1):
        a = data[i * keysize: (i+1) * keysize]
        b = data[(i+1) * keysize: (i+2) * keysize]
        blocksum += hamming(a, b)
    blocksum /= float(numblocks)
    blocksum /= float(keysize)
    return blocksum

keysize = min(range(2, 40), key=norm_dist)
print "Decided keysize = ", keysize

key = [None]*keysize

for i in range(keysize):
    d = data[i::keysize]
    key[i] = max(range(256), key=lambda k: score(xor(d, k)))

key = ''.join(map(chr, key))

print "Decided key = ", repr(key)

print "Decoded data below"
print
print ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(data, cycle(key)))
