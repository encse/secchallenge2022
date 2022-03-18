from z3 import *
from secret import test_inputs, flag

size = 64
x, y, z, t, u = BitVecs("x y z t u", size)
variables = [x, y, z, t, u]
decls = {"x": x, "y": y, "z": z, "t": t, "u": u}

def parse_smt2_ast_string(sexpr):
    s = f"(assert (= {sexpr} {sexpr}))"
    assertions = parse_smt2_string(s, decls = decls)
    return assertions[0].arg(0)

def check_eq(ast1, ast2, inputs):
    vals = list(zip(variables, [BitVecVal(inp, size) for inp in inputs]))
    return simplify(substitute(ast1, *vals)).as_long() == simplify(substitute(ast2, *vals)).as_long()

max_length = [20, 40, 70, 70]

for i in range(1, 5):
    s = open(f"mba{i}.smt2").read()
    mba = parse_smt2_ast_string(s)
    sexpr = input(f"Simplified mba {i} in smt2 format: ")
    if len(sexpr) > max_length[i-1]:
        print("Expression not simple enough!")
        exit(0)
    user_ast = parse_smt2_ast_string(sexpr)
    print(f"Checking mba {i}")
    for inp in test_inputs[i-1]:
        if not check_eq(mba, user_ast, inp):
            print("Incorrect simplification")
            exit(0)
    print("Correct!")

print(flag, flush = True)
