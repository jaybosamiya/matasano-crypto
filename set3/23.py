from mersennetwister import MT19937
from tqdm import tqdm

seed = int(raw_input('Seed? '))
discard = int(raw_input('Discard how many initial values? '))

print "[+] Made a new MT19937 generator with seed=", seed
m = MT19937(seed)

print "[+] Discarding %d values" % discard
_discarded = [m.next() for _ in tqdm(range(discard))]

print "[+] Tapping 624 new values"
vals = [m.next() for _ in range(624)]

print "[+] Cloning into new generator"
n = MT19937()
n.seed_via_clone(vals)

print "[+] Testing equality of generators"
for i in tqdm(range(2000000)):
    if m.next() != n.next():
        print " [!] Value at %d differs!!!" % i
        break
else:
    print "[+] All values checked are found same. Cheers!"
