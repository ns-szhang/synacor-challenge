def decrypt_char(reg):
    r0, r1, r2 = (reg[0], reg[1], reg[2])
    command = 'calling decrypt_char:\n'
    command += 'in : R0 = {}, R1 = {}, R2 = {}\n'.format(r0, r1, r2)
    r2 = r0 & r1
    r2 = 32768 + ~r2
    r0 = r0 | r1
    r0 = r0 & r2
    reg[0] = r0
    command += 'out : R0 = {}'.format(reg[0])
    return command


functions = {
    2125: decrypt_char
}

def call_function(addr, reg):
    if functions.get(addr) is not None:
        return functions[addr](reg)
    else:
        return False
