from common import AES_ECB_encrypt, AES_CBC_encrypt, pad

ground_truth = None             # Used only for verification


def encryption_oracle(data):
    global ground_truth         # Used only for verification
    from random import randint

    def randstr(n):
        return ''.join(chr(randint(0, 255)) for _ in range(n))

    data = randstr(randint(5, 10)) + data + randstr(randint(5, 10))
    data = pad(data)

    if randint(0, 1) == 0:
        ground_truth = 'ECB'
        return AES_ECB_encrypt(data, randstr(16))
    else:
        ground_truth = 'CBC'
        return AES_CBC_encrypt(data, randstr(16), randstr(16))


def detect_ECB_or_CBC(oracle):
    def is_ecb_encoded(s, l=16):  # Taken directly from challenge 8
        if len(s) % l != 0:
            return False
        seen = []
        for i in range(0, len(s), l):
            x = s[i:i+l]
            if x in seen:
                return True
            else:
                seen.append(x)
        return False

    value = oracle('A'*(3*16))
    if is_ecb_encoded(value):
        return 'ECB'
    else:
        return 'CBC'


def main():
    for i in range(10):
        guess = detect_ECB_or_CBC(encryption_oracle)
        if guess == ground_truth:
            print "[+] Correct.", ground_truth
        else:
            print "[-] Wrong. GT=", ground_truth, "Guess=", guess

if __name__ == '__main__':
    main()
