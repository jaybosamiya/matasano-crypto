from common import randstr, AES_CTR, xor_str
from random import randint

oracle_key = randstr(16)
oracle_nonce = randint(0, (1 << 64) - 1)


def encryption_oracle(data):
    data = data.replace(';', '').replace('=', '')
    data = "comment1=cooking%20MCs;userdata=" + data
    data = data + ";comment2=%20like%20a%20pound%20of%20bacon"
    return AES_CTR(data, oracle_key, oracle_nonce)


def decryption_oracle(data):
    dec = AES_CTR(data, oracle_key, oracle_nonce)
    return ';admin=true;' in dec


def main():
    injection_string = ';admin=true;'

    part1 = encryption_oracle('X' * len(injection_string))
    part2 = encryption_oracle('Y' * len(injection_string))
    part3 = xor_str('X' * len(injection_string), injection_string)

    locationing = xor_str(part1, part2)
    prefix_pos = locationing.index('\x01')
    suffix_pos = prefix_pos + len(injection_string)

    prefix = part1[:prefix_pos]
    mid = part1[prefix_pos:suffix_pos]
    suffix = part1[suffix_pos:]

    attack = prefix + xor_str(mid, part3) + suffix

    if decryption_oracle(attack):
        print "[+] Admin access granted"
    else:
        print "[-] Attack failed"

if __name__ == '__main__':
    main()
