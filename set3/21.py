from mersennetwister import MT19937

mt = MT19937(0)
print [mt.next() for i in range(1000)]
