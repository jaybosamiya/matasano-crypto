from common import AES_ECB_decrypt

with open('data/7.txt', 'r') as f:
    data = f.read().decode('base64')

key = "YELLOW SUBMARINE"

print AES_ECB_decrypt(data, key)
