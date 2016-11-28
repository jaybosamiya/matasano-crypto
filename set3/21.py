from mersennetwister import MT19937

mt = MT19937(0)
print [mt.extract_number() for i in range(1000)]
