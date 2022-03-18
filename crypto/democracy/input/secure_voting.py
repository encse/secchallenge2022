import math
import os
import json

from Crypto.Math.Numbers import Integer
from Crypto.Util.number import getRandomNBitInteger, isPrime, getRandomRange

"""
With some well-placed bribes an blackmail, we managed to get you some additional information about the voting system.

The code in this file is what the voting machines out in the city use to encrypt and sign partial results,
which are periodically sent over http to the main server.

We also learned the json message format, and that the last update from "dist-2472" was the following (bytes -> int, Big-endian):
b'{"district_id": "dist-2472", "results": {"Jodie Bradford": 4759, "Branden Sawyer": 3014, "Murphy Mcmillan": 2667}, "last-update": "2022-02-24T21:00:28.224995"}'

The public key parameters they use are in the key.pub.json file.

Server endpoints:
GET democracy.secchallenge.crysys.hu/results/<district>
GET democracy.secchallenge.crysys.hu/submit
POST democracy.secchallenge.crysys.hu/submit

Good luck, Agent!
"""


class SecureVoting(object):

    def __init__(self, **kwargs):
        self.rand = os.urandom

        if kwargs:
            self.N = Integer(kwargs.get('N'))
            self.p = Integer(kwargs.get('p'))
            self.k = Integer(kwargs.get('k'))
            self.q = Integer(kwargs.get('q'))
            self.g = Integer(kwargs.get('g'))
            self.x = Integer(kwargs.get('x'))
            self.y = Integer(kwargs.get('y'))

        else:
            self.N = 2048

            self.p = getRandomNBitInteger(self.N, self.rand) | 1
            while not isPrime(self.p, randfunc=self.rand):
                self.p = self.p + 2
                if self.p >= 1 << self.N:
                    self.p = (1 << self.N - 1) | 1
            self.p = Integer(self.p)

            self.k = Integer(getRandomRange(2, self.p - 2, self.rand))
            while math.gcd(self.k, self.p - 1) != 1:
                self.k = Integer(getRandomRange(2, self.p - 2, self.rand))

            self.q = Integer((self.p - 1) >> 1)

            self.g = Integer(pow(getRandomRange(Integer(2), self.p, self.rand), 2, self.p))

            self.x = Integer(getRandomRange(2, self.p - 1, self.rand))

            self.y = Integer(pow(self.g, self.x, self.p))

    def encrypt(self, m):
        c = pow(self.g, self.k, self.p)
        d = (pow(self.y, self.k, self.p) * m) % self.p
        return int(c), int(d)

    def decrypt(self, m):
        r = getRandomRange(2, self.p - 1, self.rand)
        c1 = (pow(self.g, r, self.p) * m[0]) % self.p
        c1x = pow(c1, self.x, self.p)
        plaintext_blind = (c1x.inverse(self.p) * m[1]) % self.p
        plaintext = (plaintext_blind * pow(self.y, r, self.p)) % self.p
        return int(plaintext)

    def sign(self, m):
        r = pow(self.g, self.k, self.p)
        t = (Integer(m) - self.x * r) % (self.p - 1)
        while t < 0:
            t = t + (self.p - 1)
        s = (t * self.k.inverse(self.p - 1)) % (self.p - 1)
        return int(r), int(s)

    def verify(self, m, sig):
        sig = [Integer(x) for x in sig]
        if sig[0] < 1 or sig[0] > self.p-1:
            return 0
        v1 = pow(self.y, sig[0], self.p)
        v1 = (v1 * pow(sig[0], sig[1], self.p)) % self.p
        v2 = pow(self.g, m, self.p)
        if v1 == v2:
            return 1
        return 0


with open('keys.json') as f:
    params = json.loads(f.read())
secure_voting = SecureVoting(N=params['N'],
                             p=params['p'],
                             k=params['k'],
                             q=params['q'],
                             g=params['g'],
                             x=params['x'],
                             y=params['y'])
