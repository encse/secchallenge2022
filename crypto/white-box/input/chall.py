import z3
from z3 import *
import random

size = 64
x, y, z, t, u = BitVecs("x y z t u", size)
variables = [x, y, z, t, u]
decls = {"x": x, "y": y, "z": z, "t": t, "u": u}

def rand_const():
    return BitVecVal(random.randrange(0, 2**size), size)

def parse_smt2_ast_string(sexpr):
    s = f"(assert (= {sexpr} {sexpr}))"
    assertions = parse_smt2_string(s, decls = decls)
    return assertions[0].arg(0)

def check_random_inputs(ast1, ast2):
    vals = [(v, rand_const()) for v in variables]
    return simplify(substitute(ast1, *vals)).as_long() == simplify(substitute(ast2, *vals)).as_long()

mbas = [parse_smt2_ast_string(open(f"mba{i}.smt2").read()) for i in range(1,5)]
# Tried my best, hope you can do better than z3 simplify
simplified = [z3.simplify(mba) for mba in mbas]

# sanity check
for mba, simple in zip(mbas, simplified):
    for i in range(100):
        assert(check_random_inputs(mba, simple))

for i, ast in enumerate(simplified):
    smt2_expr = " ".join(ast.sexpr().split())
    print(len(smt2_expr))
    print(smt2_expr)
