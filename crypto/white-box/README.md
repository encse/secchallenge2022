# White box

We are reversing a obfuscated program and found some incomprehensible mixed boolean-arithmetic. I have lifted it to AST and tried simplifying using z3, it didn't do much. Can you help me decode it?

`nc white-box.secchallenge.crysys.hu 5005`

Hint: [linear mba-s](https://www.usenix.org/system/files/sec21fall-liu-binbin.pdf)

*Author: Suma*

## Inputs
- [chall.py](input/chall.py)
- [mba1.smt2](input/mba1.smt2)
- [mba2.smt2](input/mba2.smt2)
- [mba3.smt2](input/mba3.smt2)
- [mba4.smt2](input/mba4.smt2)
- [server.py](input/server.py)

