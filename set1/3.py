from common import score


def decode(enc, k):
    return ''.join(chr(ord(x) ^ k) for x in enc)

enc = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'.decode('hex')
key = max(range(256), key=lambda k: score(decode(enc, k)))

print "Key: ", key
print "Decoded: ", decode(enc, key)
