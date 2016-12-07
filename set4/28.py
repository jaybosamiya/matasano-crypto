from sha import SHA1
from common import randstr

key = randstr(16)


def auth(message):
    return SHA1(key + message).hexdigest()

if __name__ == '__main__':
    print "[+] Using key =", repr(key)

    message = raw_input('[ ] Message?').strip()
    print "[+] auth(%s) = %s" % (repr(message), repr(auth(message)))
