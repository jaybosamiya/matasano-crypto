from common import randstr, AES_CBC_encrypt, AES_CBC_decrypt, pad, xor_str

oracle_key = randstr(16)
oracle_iv = oracle_key

print "[+] Oracle Key =", repr(oracle_key)


def encryption_oracle(data):
    data = data.replace(';', '').replace('=', '')
    data = "comment1=cooking%20MCs;userdata=" + data
    data = data + ";comment2=%20like%20a%20pound%20of%20bacon"
    data = pad(data)
    return AES_CBC_encrypt(data, oracle_key, oracle_iv)


def decryption_oracle(data):
    dec = AES_CBC_decrypt(data, oracle_key, oracle_iv)
    if not all(ord(c) < 0x80 for c in dec):
        raise ValueError('%s contains high-ASCII' % repr(dec))
    return ';admin=true;' in dec


def main():
    print "[+] Starting attack..."

    block_len = 16
    val = encryption_oracle('')
    assert(len(val) > 3 * block_len)  # If not, then we'd have sent a
                                      # larger string to the
                                      # encryption_oracle

    c1 = val[:block_len]
    attack = c1 + '\x00'*block_len + c1

    try:
        decryption_oracle(attack)
        print "[!] Damn, no exception was thrown. Attack failed :("
    except ValueError as v:
        ret = eval(v.message[:-len(' contains high-ASCII')])
        key = xor_str(ret[:block_len],
                      ret[2*block_len:3*block_len])
        print "[+] Found key =", repr(key)
        if key == oracle_key:
            print "[+] Attack successful"
        else:
            print "[+] Failed attack :("


if __name__ == '__main__':
    main()
