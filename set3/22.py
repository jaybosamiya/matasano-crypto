from mersennetwister import MT19937
from random import randint
from time import sleep, time

def get_randout():
    global SEED_VAL             # Only used for verification
    sleep(randint(40, 1000))
    seed = int(time())
    SEED_VAL = seed
    sleep(randint(40, 1000))
    return MT19937(seed).next()


def crack(output, time_range=2000):
    now = int(time())

    possible_seeds = []
    for seed in range(now - time_range, now + time_range):
        if MT19937(seed).next() == output:
            possible_seeds.append(seed)

    return possible_seeds


out = get_randout()
print "PRNG Output:", out

seeds = crack(out)
print "Cracked possible seeds:", seeds

if SEED_VAL in seeds:
    print "Worked!"
else:
    print "Something somewhere went terribly wrong."
