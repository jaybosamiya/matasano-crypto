from common import AES_CTR

data = 'L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=='.decode('base64')

print repr(AES_CTR(data, 'YELLOW SUBMARINE', 0))
