"""A generalized Mersenne Twister module.

Provides a MersenneTwister class, and a MT19937 class which
instantiates MersenneTwister with the appropriate standard constants
used for MT19937.

Reference Pseudocode taken from https://en.wikipedia.org/wiki/Mersenne_Twister

"""


def _low_bits(k, n):
    """Return lowest k bits of n."""
    return (((1 << k) - 1) & n)


class MersenneTwister:
    """A generalized Mersenne Twister class.

    Example usage:

    >>> mt = MersenneTwister(...).seed(0)
    >>> mt.extract_number()

    """

    def __init__(self, w, n, m, r, a, u, d, s, b, t, c, l, f):
        """Set up internal state to say that it is not seeded."""
        self.MT = [0]*n
        self.index = n+1
        self.lower_mask = (1 << r) - 1
        self.upper_mask = _low_bits(w, ~ self.lower_mask)
        self.w = w
        self.n = n
        self.m = m
        self.r = r
        self.a = a
        self.u = u
        self.d = d
        self.s = s
        self.b = b
        self.t = t
        self.c = c
        self.l = l
        self.f = f

    def seed(self, seed):
        """Initialize the generator from the seed."""
        self.index = self.n
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = _low_bits(self.w,
                                   (self.f *
                                    (self.MT[i-1] ^
                                     (self.MT[i-1] >> (self.w-2))) + i))

    def twist(self):
        """Generate the next n values from the series x_i.

        This is mainly meant for internal usage. Not to be used
        externally unless you know what you are doing.

        """
        for i in range(self.n):
            x = ((self.MT[i] & self.upper_mask) +
                 (self.MT[(i+1) % self.n] & self.lower_mask))
            xA = (x >> 1)
            if x % 2 != 0:
                xA = xA ^ self.a
            self.MT[i] = self.MT[(i + self.m) % self.n] ^ xA
        self.index = 0

    def extract_number(self):
        """Extract a tempered value based on MT[index].

        Calls twist() every n numbers.

        """
        if self.index >= self.n:
            if self.index > self.n:
                print "Generator was never seeded"
            self.twist()

        y = self.MT[self.index]
        y = y ^ ((y >> self.u) & self.d)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)
        y = y ^ (y >> self.l)

        self.index += 1
        return _low_bits(self.w, y)


class MT19937:
    """Generate a MT19937 Mersenne Twister."""

    def __init__(self, seed):
        """Initialize with a seed."""
        w = 32
        n = 624
        m = 397
        r = 31
        a = 0x9908B0DF
        u = 11
        d = 0xFFFFFFFF
        s = 7
        b = 0x9D2C5680
        t = 15
        c = 0xEFC60000
        l = 18
        f = 1812433253
        self.mt = MersenneTwister(w, n, m, r, a, u, d, s, b, t, c, l, f)
        self.mt.seed(seed)

    def extract_number(self):
        """Generate next value."""
        return self.mt.extract_number()
