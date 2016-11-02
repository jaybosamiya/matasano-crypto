from common import randstr


def parse(data):
    data = data.split('&')
    data = [x.split('=') for x in data]
    ret = {k: v for k, v in data}
    return ret


# Oracles

oracle_key = randstr(16)


def profile_for(email):
    from common import AES_ECB_encrypt, pad
    email = email.replace('=', '').replace('&', '')
    profile = 'email=' + email + '&uid=10&role=user'
    return AES_ECB_encrypt(pad(profile), oracle_key)


def user_profile(enc):
    from common import AES_ECB_decrypt, unpad
    return parse(unpad(AES_ECB_decrypt(enc, oracle_key)))


# Attack


def main():
    # 0123456789abcdef0123456789abcdef0123456789abcdef
    # email=XXXXXXXXXXXXX&uid=10&role=user <--------------------- (1)
    # email=XXXXXXXXXXadmin...........&uid=10&role=user <-------- (2)
    # email=XXXXXXXXXXXXX&uid=10&role=admin........... <--------- (attack)

    from common import pad

    r1 = profile_for('XXXXXXXXXXXXX')
    r2 = profile_for('XXXXXXXXXX' + pad('admin'))

    attack = r1[:32] + r2[16:32]

    print user_profile(attack)

if __name__ == '__main__':
    main()
