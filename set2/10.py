from common import AES_CBC_decrypt

with open('data/10.txt', 'r') as f:
    data = f.read().decode('base64')

print AES_CBC_decrypt(data, "YELLOW SUBMARINE", '\x00' * 16)
