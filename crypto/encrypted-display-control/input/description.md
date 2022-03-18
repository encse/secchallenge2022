Encrypted display control
=========================

A small matrix display is driven by a sequence of single-byte control commands. Four special commands control a cursor:

	\x00 - move cursor right
	\x01 - move cursor left
	\x02 - move cursor down
	\x03 - move cursor up

In addition, ascii codes are interpreted as commands that print the character defined by the code on the display at the current location of the cursor.

The following Python function simulates the operation of the display: 

```python
def display(ctrl_seq):

	D = []
	for i in range(10):
		d = []
		for j in range(180):
			d.append(' ')
		D.append(d)

	i, j = 0, 0
	for c in ctrl_seq:
		if c == 0: j += 1
		elif c == 1: j -= 1
		elif c == 2: i += 1
		elif c == 3: i -= 1
		else: D[i][j] = chr(c)

	for i in range(10):
		for j in range(180):
			print(D[i][j], end='')
		print('')
```

For instance, if the input is the control sequence `\x61 \x00 \x62 \x00 \x63`, then 'abc' is printed in the upper left corner of the display.

The display can be remotely controlled by sending a control sequence to it using a cryptographic protocol, which works as follows:  

- Each control command C is preceded by a 2-byte sequence number SQN (in big-endian):

		+---+---+---+
		|  SQN  | C |
		+---+---+---+

- Sequence numbering begins with 0, and numbered commands are concatenated in a plaintext stream. For instance, the above command sequence results in the following plaintext stream:

		+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+
		|x00 x00|x61|x00 x01|x00|x00 x02|x62|x00 x03|x00|x00 x04|x63|
		+---+---+---+---+---+---+---+---+---+---+---+---+---+---+---+

- Finally, the plaintext stream is encrypted with a proprietary stream cipher, and the resulting ciphertext is sent to the display.

The proprietary stream cipher uses the `get_random_bytes()` function of the following pseudo-random generator to generate a key stream (of the same length as the plaintext stream), which is then XORed to the plaintext stream.

```python
from Crypto.Hash import MD5  # use MD5 from the PyCryptodome library

class PRNG:
	prng_glen = None
	prng_state = None
	prng_buffer = None

	def __init__(self):
		self.prng_glen = 16
		self.prng_state = b''
		self.prng_buffer = b''

	def rot_byte(self, b):
		f = b%2
		r = b//2
		if f: r = r|0b10000000
		return r

	def rot_block(self, B):
		R = B[-1:]+B[:-1] 
		return R

	def shuffle_block(self, B):
		R = b''
		for i in range(len(B)):
			r = B[i]
			for j in range(i): r = self.rot_byte(r)
			R += r.to_bytes(1, 'big')
		R = self.rot_block(R)
		return R

	def update_state_and_generate(self):
		self.prng_state = self.shuffle_block(self.prng_state)
		h = MD5.new()
		h.update(self.prng_state)
		return(h.digest())

	def seed(self, s):
		h = MD5.new()
		h.update(s)
		self.prng_state = h.digest()[4:12]

	def get_random_bytes(self, n):

		if n < 0: return(b'')

		l = len(self.prng_buffer)
		if n > l:  # not enough bytes in buffer, we need to generate more
			for i in range(1+(n-l)//self.prng_glen):
				self.prng_buffer += self.update_state_and_generate()
		
		# enough bytes in buffer 
		r = self.prng_buffer[:n]  # will return first n bytes from buffer
		self.prng_buffer = self.prng_buffer[n:]  # remove first n bytes from buffer
		return r
```

You intercepted a control secquence encrypted as described above (see `proto_msgs.crypt`). Recover the plaintext stream, extract the control sequence from it, and use the display simulator to get the flag!
