def is_ecb_encoded(s, l=16):
    if len(s) % l != 0:
        return False
    seen = []
    for i in range(0, len(s), l):
        x = s[i:i+l]
        if x in seen:
            return True
        else:
            seen.append(x)
    return False

with open('data/8.txt', 'r') as f:
    data = f.read().split()

for i, d in enumerate(data):
    if is_ecb_encoded(d):
        print i, d
        print
