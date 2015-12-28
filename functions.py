import sys

def _display_string(starting_addr, func, mod, read):
    length = read(starting_addr)
    for i in range(length):
        if func == 1531:
            _display_char(read(starting_addr + i + 1), mod)
        else:
            raise Exception('unimplemented string display {}'.format(func))
    return length
def display_string(reg, machine):
    if reg[1] not in [1531]:
        return False
    reg[1] = _display_string(reg[0], reg[1], reg[2], machine.read_address)
    return True

def _display_char(char, mod):
    char = _decrypt_char1(char, mod)
    sys.stdout.write(chr(char))
    return char
def display_char(reg, machine):
    reg[0] = _display_char(reg[0], reg[2])
    return True

def _decrypt_char1(val, c1):
    c2 = val & c1
    c2 = 32768 + ~c2
    val = val | c1
    val = val & c2
    return val
def decrypt_char1(reg, machine):
    # raise Exception('decrypt_char1 called')
    reg[0] = _decrypt_char1(reg[0], reg[1])
    return True


functions = {
    1458: display_string,
    1531: display_char,
    2125: decrypt_char1
}

def print_reg(reg):
    output = 'addr: {} '.format(reg['addr'])
    for i in range(8):
        output += '{}:{} '.format(i, reg[i])
    return output

def call_function(addr, reg, machine):
    if functions.get(addr) is not None:
        function = functions[addr]
        command = 'calling {}:\n'.format(function.__name__)
        command += ' in:  {}\n'.format(print_reg(reg))
        ret = function(reg, machine)
        command += ' out: {}\n'.format(print_reg(reg))
        if ret == False:
            return False
        return command
    else:
        return False
