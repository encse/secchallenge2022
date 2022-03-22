# Encrypted Display Control

Let's check the PRNG first. It has a seed function that takes some arbitrary value, calculates its md5 hash
and takes bytes [4:12] out of the digest. This is stored in the prng_state variable:

```python
def seed(self, s):
    h = MD5.new()
    h.update(s)
    self.prng_state = h.digest()[4:12]
```

`get_random_bytes(self, n)` can be used to retrieve an arbitrary number of pseudo random bytes. The class
has an inner `prng_buffer` which stores the leftorver bytes (bytes that were calculated but not returned) 
from previous invocations of this function.

The actual generation has two steps and implemented in `update_state_and_generate`. First `prng_state` 
gets updated with shuffling its own bits. Then the new `prng_state` is hashed with MD5 and
the result is appended to `prng_buffer`.

```python
def update_state_and_generate(self):
    self.prng_state = self.shuffle_block(self.prng_state)
    h = MD5.new()
    h.update(self.prng_state)
    return(h.digest())
```

`get_random_bytes(self, n)` calls `update_state_and_generate` in a loop until it has enough bytes in the buffer
and takes the first n out of it.

## How do we crack this?

Closer observation of the `shuffle_block` function 
reveals that `prng_state` has a 16 long loop. This also means 
the period of the encryption key is 256 bytes.

We also know every first and second bytes 
modulo 3 of the plaintext so it's possible to find
the corresponding key bytes with xoring the ciphertext
and the plaintext. 

In the second period of the key the know plaintext bytes are shifted 
by one (since 256 not divisble by 3) giving us a chance to 
figure out the rest of the key.

Next decipher the plaintext.

Finally run the provided display routine on it.
