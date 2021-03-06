
# VPScoin

VPScoin was a warmed up edition of a challenge from 2020. According to the organizes, the original had a few bugs in it, which let some people solve it the unintended way.

This challenge was about MD5 collision generation. There are three different ways of doing this that I know about:

- given an arbitrary input, extend it with two different suffixes so that the results have the same MD5 signature. This can be generated almost instantly.
- given two different inputs, extend them with suffixes so that the results has the same signature. This takes a few days or week.
- given an arbitrary input, change a few bits in it in fixed locations. Then generate suffixes so that the two inputs have the same signature. This takes about 10-15 minutes.

The exact requirements are more obscure, but this is the idea. We had to use the third version. 

But what is it good for? 

We have a programming language with conditional jumps. If we can set up an input so that changing just one bit triggers a different codepath, we can use a collision generator to create an innocent version first, send it to the server. Then upload the evil one which has the same MD5 signature.

The tool I used is called [hashclash](https://github.com/cr-marcstevens/hashclash), it can change the 10th byte's least significant bit and generate a collision for the two inputs.

The 'program' I went with was something like:

```
nicebinary = (
        apikey+b"\x10\x05" +  # store 5
        apikey+b"\x10\x04" +  # store 4
        apikey+b"\x30\x04" +  # cmp 4
        apikey+b"\x42\x69" +  # flag1
        apikey+b"\x30\x04" +  # cmp 4
        apikey+b"\x69\x42" +  # flag2
        apikey+b"\x20\x00"    # print
    )
```

Note that `apikey` is 6 bytes, so each 'statement' takes 8 bytes. If we feed this into the collision generator it will change the `apikey` of the second statement making it an invalid one, which will be ignored by the server side interpreter. (It just throws away statements with invalid api keys.)

We have the two different programs. The 'good' one just prints 5, the second one however runs the `flag1` and `flag2` statements.
 
I wrote nicebinary to a file then ran hashclash with:

```
> scripts/poc_no.sh nicebinary
```

at first I thought I need to change `scripts/poc_no.sh`, but at the and I could just it use as it is. It was not instant. I had to wait from a few minutes to 15 minutes until it found something. It's like a halting problem, you never know if it will finish or you didn't set it up properly. It takes some practicing to get it right...

The last twist is that you cannot give the whole `nicebinary` to `poc_no.sh` because it will just never find a collision. I think too many bits are fixed from a 64 bytes long MD5 block, and it just cannot find its way to extend it properly. 

You need to cut `nicebinary` into two pieces. The first 16 bytes and the rest. Give the first slice to `poc_no.sh`, which extends it with some garbage, then append the rest of `nicebinary` to the end. The payloads will have the following structure:

```
     
    0000  stm1 stm2             +
    0010  garbage               |
    0020  garbage               |   full MD5 block
    0030  garbage               +

    0040  garbage               +
    0050  garbage               | 
    0060  garbage               |   full MD5 block
    0070  garbage               +

    0080  stm3 stm4             
    0090  stm5 stm6             
    00a0  stm7                  

```

We will have two different versions of the first two blocks that have the same MD5 signature. This is generated by hashclash. We can freely append anything to this, it will result in a different MD5 hash, but the same one for both inputs.
