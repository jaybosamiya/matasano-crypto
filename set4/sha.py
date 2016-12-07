"""SHA-1 implementation.

Reference pseudocode taken from Wikipedia [1]

[1] https://en.wikipedia.org/wiki/SHA-1

"""


def _lrot32(val, rot):
    ret = (val << rot) | (val >> (32 - rot))
    return ret & 0xffffffff


class SHA1:
    r"""
    SHA1 Class.

    Usage:
    >>> sha = SHA1("The quick brown fox jumps over the lazy dog")
    >>> sha.hexdigest()
    '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12'
    >>> sha.digest()
    '/\xd4\xe1\xc6z-(\xfc\xed\x84\x9e\xe1\xbbv\xe79\x1b\x93\xeb\x12'

    >>> sha = SHA1()
    >>> sha.update("The quick brown fox jumps")
    >>> sha.update(" over the lazy dog")
    >>> sha.hexdigest()
    '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12'

    """

    def __init__(self, data=''):
        """Initialize SHA1 class."""
        self.h0 = 0x67452301
        self.h1 = 0xEFCDAB89
        self.h2 = 0x98BADCFE
        self.h3 = 0x10325476
        self.h4 = 0xC3D2E1F0

        self.data = [data[:]]   # Copy stored as a list to speed up
                                # repeated updates

    def update(self, data):
        """Add more data to the class."""
        self.data.append(data[:])  # Append a copy
        return self

    def digest(self):
        """Generate SHA1 digest."""
        import struct

        h0 = self.h0
        h1 = self.h1
        h2 = self.h2
        h3 = self.h3
        h4 = self.h4

        # Pre-processing

        data = ''.join(self.data)
        ml = 8 * len(data)

        data += '\x80'
        data += '\x00' * ((56 - len(data)) % 64)
        data += struct.pack('>Q', ml)

        assert(len(data) % 64 == 0)

        # Process message in successive 512-bit chunks

        for chunk_idx in xrange(0, len(data), 64):
            chunk = data[chunk_idx:chunk_idx + 64]
            w = [struct.unpack('>I', chunk[i:i+4])[0]
                 for i in xrange(0, 64, 4)]
            for i in xrange(16, 80):
                w_i = _lrot32(w[i-3] ^ w[i-8] ^ w[i-14] ^ w[i-16], 1)
                w.append(w_i & 0xffffffff)

            # Initialize hash value for this chunk
            a = h0
            b = h1
            c = h2
            d = h3
            e = h4

            # Main loop
            for i in xrange(0, 80):
                if 0 <= i <= 19:
                    f = (b & c) | ((~b) & d)
                    k = 0x5A827999
                elif 20 <= i <= 39:
                    f = b ^ c ^ d
                    k = 0x6ED9EBA1
                elif 40 <= i <= 59:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8F1BBCDC
                elif 60 <= i <= 79:
                    f = b ^ c ^ d
                    k = 0xCA62C1D6
                else:
                    assert(False)  # Should not be reached

                temp = _lrot32(a, 5) + f + e + k + w[i]
                temp &= 0xffffffff
                e = d
                d = c
                c = _lrot32(b, 30)
                b = a
                a = temp

            # Add this chunk's hash to result so far
            h0 = (h0 + a) & 0xffffffff
            h1 = (h1 + b) & 0xffffffff
            h2 = (h2 + c) & 0xffffffff
            h3 = (h3 + d) & 0xffffffff
            h4 = (h4 + e) & 0xffffffff

        # Produce final hash value
        hh = (struct.pack('>I', h0) +
              struct.pack('>I', h1) +
              struct.pack('>I', h2) +
              struct.pack('>I', h3) +
              struct.pack('>I', h4))

        return hh

    def hexdigest(self):
        """Generate SHA1 Digest in hexadecimal."""
        return self.digest().encode('hex')

if __name__ == '__main__':
    empty_digest = 'da39a3ee5e6b4b0d3255bfef95601890afd80709'
    assert(SHA1('').hexdigest() == empty_digest)
    message = "The quick brown fox jumps over the lazy dog"
    digest = '2fd4e1c67a2d28fced849ee1bb76e7391b93eb12'
    assert(SHA1(message).hexdigest() == digest)
    assert(SHA1().update(message).hexdigest() == digest)
    assert(SHA1().update(message[:5]).update(message[5:]).hexdigest()
           == digest)
    print "[+] All tests passed"
