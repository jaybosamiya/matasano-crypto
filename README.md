Matasano Crypto Challenges Solutions
====================================

The guys over at Matasano have made a set of [48 challenges](http://cryptopals.com/) that show attacks on real-world crypto.
This repository contains solutions to the challenges, as and when I solve them.

I had started [another repository](https://github.com/jaybosamiya/cryptopals-solutions/) earlier, but a whole bunch of that code is badly written, and I decided to start over from scratch.

All the solutions in this repository have been written in Python 2.7, and can be found by going to the correct set number.

Each of the sets has a `common.py` file, which contains code that is re-used in that set. Different sets can have extremely different `common.py` files, and need _not_ be subset/superset of each other.

License
-------

Everything in this repository is covered under the [MIT License](http://jay.mit-license.org/2016).

Solutions:
----------

1. [Convert hex to base64](set1/1.py)
2. [Fixed XOR](set1/2.py)
3. [Single-byte XOR cipher](set1/3.py)
4. [Detect single-character XOR](set1/4.py)
5. [Implement repeating-key XOR](set1/5.py)
6. [Break repeating-key XOR](set1/6.py)
7. [AES in ECB mode](set1/7.py)
8. [Detect AES in ECB mode](set1/8.py)
9. [Implement PKCS#7 padding](set2/9.py)
10. [Implement CBC mode](set2/10.py)
11. [An ECB/CBC detection oracle](set2/11.py)
12. [Byte-at-a-time ECB decryption (Simple)](set2/12.py)
