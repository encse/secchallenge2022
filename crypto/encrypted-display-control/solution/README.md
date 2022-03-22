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

Closer observation of the `shuffle_block` function reveals that `prng_state` has a 16 long loop. Which means the actual key bytes that we use for encryption are repeated after 256 bytes. Combined this with the fact that we know every first and second bytes modulo 3 of the plaintext and 
in the second period of the key the plaintext bytes are shifted by one, we can figure out the key bytes by xoring the plaintext and the ciphertext first. Then using the decrypted key to decrypt the remaining parts of the plaintext.
