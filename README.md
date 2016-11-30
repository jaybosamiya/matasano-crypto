Matasano Crypto Challenges Solutions
====================================

The guys over at Matasano have made a set of [48 challenges](http://cryptopals.com/) (split over 6 sets) that show attacks on real-world crypto. Sets 7 and 8 were added later, btw, by them.

This repository contains solutions to the challenges (as well as the challenge statements), as and when I solve them.

I had started [another repository](https://github.com/jaybosamiya/cryptopals-solutions/) earlier, but a whole bunch of that code is badly written, and I decided to start over from scratch.

Challenges and Solutions
------------------------

1. [Basics](set1)
2. [Block crypto](set2)
3. [Block & stream crypto](set3)
4. [Stream crypto and randomness](set4)

Each of the sets contain solutions in the `#.py` files (Python 2.7), as well as the questions in the `README.md` of the appropriate directory. You can jump to a solution by clicking on the heading of any of the challenges.

Additionally the sets each have a `common.py` file, which contains code that is re-used in that set. Different sets can have extremely different `common.py` files, and need _not_ be subset/superset of each other.

License
-------

All code in this repository is covered under the [MIT License](http://jay.mit-license.org/2016).

The questions are taken from [cryptopals.com](http://cryptopals.com/). No infringement is intended.
