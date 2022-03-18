from flag import FLAG

def runcode(scode, api_key, sandbox):

    opcodes = {
        0x10: "store",
        0x20: "print",
        0x30: "cmp",
        0x42: "flag1",
        0x69: "flag2",
    }

    pc = 0
    register = 0
    flag_primed = False
    output = ""
    while pc < len(scode):
        api_key_ok = True
        for j in range(len(api_key)):
            if scode[pc+j] != api_key[j]:
                api_key_ok = False
                break
        if not api_key_ok:
            if pc == 0:
                return {False, "api key bad"}
            pc += 1
            continue

        try:
            op = opcodes[scode[pc+len(api_key)]]
        except KeyError:
            return {False, "invalid opcode"}
        op2 = scode[pc+len(api_key)+1]

        if "flag" in op:
            if sandbox:
                return {False, "flag opcode"}
            else:
                if op2 not in opcodes and "flag" not in opcodes[op2] or op == opcodes[op2]:
                    return {False, "invalid opcode"}
                if op == "flag1":
                    flag_primed = True
                    output += "Flag loaded!\n"
                if op == "flag2" and flag_primed:
                    output += f"Here is your flag: {FLAG}\n"
            pc += 8
            continue

        if op == "store":
            register = op2
            pc += 8
            continue

        if op == "print":
            output += f"Printing stored value: {register}\n"
            pc += 8
            continue

        if op == "cmp":
            if register == op2:
                pc += 8
            pc += 8
            continue

    return {True, output}


if __name__ == "__main__":
    apik = b"\x01\x02\x03\x04\x05\x06"
    print(runcode(
        apik+b"\x10\x04" +  # store 4
        apik+b"\x20\x00" +  # print
        apik+b"\x30\x05" +  # cmp 5
        apik+b"\x42\x69" +  # flag1
        apik+b"\x30\x05" +  # cmp 5
        apik+b"\x69\x42" +  # flag2
        apik+b"\x20\x00",  # print
        apik, False))

    print(runcode(
        apik+b"\x10\x04" +  # store 4
        apik+b"\x20\x00" +  # print
        apik+b"\x30\x05" +  # cmp 5
        apik+b"\x42\x69" +  # flag1
        apik+b"\x30\x05" +  # cmp 5
        apik+b"\x69\x42" +  # flag2
        apik+b"\x20\x00",  # print
        apik, True))

    print(runcode(
        apik+b"\x10\x04" +  # store 4
        apik+b"\x20\x00" +  # print
        apik+b"\x30\x04" +  # cmp 4
        apik+b"\x42\x69" +  # flag1
        apik+b"\x30\x04" +  # cmp 4
        apik+b"\x69\x42" +  # flag2
        apik+b"\x20\x00",  # print
        apik, False))

    print(runcode(
        apik+b"\x10\x04" +  # store 4
        apik+b"\x20\x00" +  # print
        apik+b"\x30\x04" +  # cmp 4
        apik+b"\x42\x69" +  # flag1
        apik+b"\x30\x04" +  # cmp 4
        apik+b"\x69\x42" +  # flag2
        apik+b"\x20\x00",  # print
        apik, True))

    print(runcode(
        b"xx" +
        apik+b"\x10\x04" +  # store 4
        apik+b"\x20\x00" +  # print
        apik+b"\x30\x04" +  # cmp 4
        apik+b"\x42\x69" +  # flag1
        apik+b"\x30\x04" +  # cmp 4
        apik+b"\x69\x42" +  # flag2
        apik+b"\x20\x00",  # print
        apik, True))

    print(runcode(
        b"xx" +
        apik+b"\x10\x04" +  # store 4
        apik+b"\x20\x00" +  # print
        apik+b"\x30\x04" +  # cmp 4
        apik+b"\x42\x69" +  # flag1
        apik+b"\x30\x04" +  # cmp 4
        apik+b"\x69\x42" +  # flag2
        apik+b"\x20\x00",  # print
        apik, True))


