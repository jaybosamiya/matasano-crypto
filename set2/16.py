from common import randstr, AES_CBC_encrypt, AES_CBC_decrypt, pad, xor_str

oracle_key = randstr(16)
oracle_iv = randstr(16)


def encryption_oracle(data):
    data = data.replace(';', '').replace('=', '')
    data = "comment1=cooking%20MCs;userdata=" + data
    data = data + ";comment2=%20like%20a%20pound%20of%20bacon"
    data = pad(data)
    return AES_CBC_encrypt(data, oracle_key, oracle_iv)


def decryption_oracle(data):
    dec = AES_CBC_decrypt(data, oracle_key, oracle_iv)
    return ';admin=true;' in dec


def main():
    prefix_only = encryption_oracle("")
    value = encryption_oracle("A" * (16 * 3))
    for i in range(0, len(prefix_only), 16):
        if prefix_only[i:i + 16] != value[i:i + 16]:
            attack = value[:i]
            attack += xor_str(
                value[i:i + 16], xor_str(';admin=true;xxxx', 'A' * 16))
            attack += value[i + 16:]
            break
    if decryption_oracle(attack):
        print "[+] Admin access granted"
    else:
        print "[-] Attack failed"

if __name__ == '__main__':
    main()
