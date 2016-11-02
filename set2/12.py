from common import AES_ECB_encrypt, pad
from random import randint


def randstr(n):
    return ''.join(chr(randint(0, 255)) for _ in range(n))


oracle_key = randstr(16)


def ecb_oracle(data):
    data += (
        """
        Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
        aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
        dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
        YnkK
        """.decode('base64'))
    data = pad(data)
    return AES_ECB_encrypt(data, oracle_key)


def get_block_size(oracle):
    i = 0
    prev_len = len(oracle(''))
    while True:
        i += 1
        new_len = len(oracle('A' * i))
        if new_len > prev_len:
            return new_len - prev_len


def get_hidden_data_len(oracle):
    prev = len(oracle(''))
    i = 0
    while True:
        i += 1
        if len(oracle('a' * i)) > prev:
            return prev - i


def byte_at_a_time_decrypt(oracle):
    block_size = get_block_size(oracle)
    known = ''
    for _ in range(get_hidden_data_len(oracle)):
        prior = 'A' * ((block_size - len(known) - 1) % block_size)
        enc_len = len(prior) + len(known) + 1
        assert(enc_len % block_size == 0)
        prior_enc = oracle(prior)[:enc_len]
        for i in range(256):
            post = prior + known + chr(i)
            post_enc = oracle(post)[:enc_len]
            if prior_enc == post_enc:
                known += chr(i)
                break
    return known


if __name__ == '__main__':
    print byte_at_a_time_decrypt(ecb_oracle)
