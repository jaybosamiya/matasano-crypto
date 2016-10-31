from common import score
from tqdm import tqdm  # For progress bar


def decode(enc, k):
    return ''.join(chr(ord(x) ^ k) for x in enc)

with open('data/4.txt', 'r') as f:
    data = f.read().split()
    data = [d.decode('hex') for d in data]

keys = [max(range(256), key=lambda k: score(decode(e, k))) for e in tqdm(data)]
decs = [decode(e, k) for e, k in zip(data, keys)]

best = max(decs, key=score)

print best
