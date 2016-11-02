from common import AES_ECB_encrypt, pad, randstr
from random import randint


oracle_key = randstr(16)
random_prefix = randstr(randint(3, 255))


def ecb_oracle(data):
    data += (
        """
        Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
        aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
        dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
        YnkK
        """.decode('base64'))
    data = random_prefix + data
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


# Return a new oracle with the prefix removed
# This is the ONLY change from challenge 12, with respect to the attack
# Wrap this around the oracle, to get a new oracle on which to run old attack
def remove_prefix(oracle):
    block_size = get_block_size(oracle)

    def get_info():
        prefixer = '\x00' * (3 * block_size)
        i = 0
        while True:
            enc = oracle(prefixer + '\x00' * i)
            for j in range(0, len(enc) - 2 * 16, 16):
                if enc[j:j+16] == enc[j+16:j+32] == enc[j+32:j+48]:
                    return (prefixer + '\x00'*i, j+48)
            i += 1

    prefix, split_point = get_info()

    def new_oracle(data):
        return oracle(prefix + data)[split_point:]

    return new_oracle


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
    print byte_at_a_time_decrypt(remove_prefix(ecb_oracle))
