from common import xor_str
from mersennetwister import MT19937
from tqdm import tqdm


def stream_cipher(seed, data):
    assert(seed.bit_length() <= 16)

    def stream():
        mt = MT19937(seed)
        while True:
            x = mt.next()
            for i in xrange(4):
                yield chr(x & 0xff)
                x = (x >> 8)

    return xor_str(data, stream())


# Verifying correctness
if (stream_cipher(10, stream_cipher(10, 'aaa')) != 'aaa'):
    import sys
    print "[!] Something somewhere went terribly wrong"
    sys.exit(1)


# Actual oracle

def oracle(data):
    global SEED                 # Used only for verification

    from common import randstr
    from random import randint

    p = randstr(randint(5, 50)) + data
    s = randint(0, (1 << 16) - 1)
    SEED = s
    return stream_cipher(s, p)

# Actual attack

LEN_PLAINTEXT = 14
ciphertext = oracle('A'*LEN_PLAINTEXT)
keys = []
for k in tqdm(xrange(1 << 16)):
    if stream_cipher(k, ciphertext)[-LEN_PLAINTEXT:] == 'A'*LEN_PLAINTEXT:
        keys.append(k)

print "[+] SEED =", SEED
print "[+] keys =", keys

if SEED in keys:
    print "[+] Success!"
else:
    print "[!] Fail!"
