from __init__ import operations
from vm import VirtualMachine
import sys

def trace(machine, addr, memo=None):
    '''
    Given an address, print out all following machine language commands
    until a 'ret' operation is reached.

    A 'jmp', 'jt' or 'jf' call indicates a fork. If a fork is hit, also
    trace out the address being jumped to.
    '''
    print 'tracing address {}'.format(addr)
    def parse(n):
        if n >= 0 and n < 32768:
            return str(n)
        elif n >= 32768 and n < 32776:
            return 'R' + str(n - 32768)
        else:
            raise Exception('Invalid n')

    if memo == None:
        memo = {}

    forks = []

    while True:
        if memo.get(addr) is not None:
            break
        inst = machine.read_address(addr)
        if inst in operations.keys():
            op, n_args = operations[inst]
            args = [op]
            for i in range(n_args):
                arg = parse(machine.read_address(addr + 1 + i))
                args.append(arg)

            if op == 'jmp':
                forks.append(int(args[1]))
            if op in ['jt', 'jf']:
                forks.append(int(args[2]))
            elif op == 'out' and args[1][0] != 'R'  :
                args.append(chr(int(args[1])))
            memo[addr] = ' '.join(args)

            if op == 'ret':
                break
            addr += 1 + n_args
        else:
            addr += 1
    for fork in forks:
        trace(machine, fork, memo)
    return memo


if __name__ == '__main__':
    addr = int(sys.argv[1])
    machine = VirtualMachine('input/challenge.bin')
    machine.load_state('teleporter')

    output = trace(machine, addr)

    for key in sorted(output.keys()):
        print "{}: {}".format(key, output[key])
