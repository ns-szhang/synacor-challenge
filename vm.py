import struct
import sys

from functions import call_function

SHOW_MESSAGES = False

def debug(msg):
    if SHOW_MESSAGES:
        print msg


class VM:
    def __init__(self, input_file):
        with open(input_file, 'rb') as file:
            self.memory = file.read()
        self.cached_memory = {}
        self.reg = {
            'addr': 0,
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0
        }
        self.stack = []

    def load_state(self, save_name='save'):
        with open(save_name + '/register', 'r') as file:
            inputs = file.read().rstrip().split('\n')
        for input in inputs:
            args = input.split()
            if args[0] == 'addr':
                self.reg['addr'] = int(args[1]) - 1
            else:
                self.reg[int(args[0])] = int(args[1])

        with open(save_name + '/stack', 'r') as file:
            inputs = file.read().rstrip().split('\n')
        for input in inputs:
            self.stack.append(int(input))

        with open(save_name + '/memory', 'r') as file:
            inputs = file.read().rstrip().split('\n')
        for input in inputs:
            args = input.split()
            self.cached_memory[int(args[0])] = int(args[1])

    def save_state(self):
        with open('register', 'w') as file:
            for key, value in self.reg.iteritems():
                file.write("{} {}\n".format(key, value))

        with open('stack', 'w') as file:
            for i in self.stack:
                file.write('{}\n'.format(i))

        with open('memory', 'w') as file:
            for k, v in self.cached_memory.iteritems():
                file.write('{} {}\n'.format(k, v))

    def _read_next(self):
        val = self.read_address(self.reg['addr'])
        self.reg['addr'] += 1
        return val

    def _parse_address(self):
        value = self._read_next()
        if value >= 32768 and value <= 32775:
            return value - 32768
        else:
            raise Exception('Invalid address')

    def _parse_value(self):
        value = self._read_next()
        if value >= 0 and value <= 32767:
            return value
        if value >= 32768 and value <= 32775:
            debug("reading from register {} = {}".format(
                value - 32768, self.reg[value - 32768]))
            return self.reg[value - 32768]
        else:
            raise Exception('Invalid value')

    def read_address(self, address):
        if self.cached_memory.get(address) is None:
            return struct.unpack(
                '<H', self.memory[2*address:2*address+2])[0]
        return self.cached_memory[address]

    def run_next_instruction(self):
        addr = self.reg['addr']
        inst = self._read_next()
        command = ''

        if inst == 0:
            command = 'stop'

        elif inst == 1:
            arg1 = self._parse_address()
            arg2 = self._parse_value()
            command = 'set R{} {}'.format(arg1, arg2)
            self.reg[arg1] = arg2

        elif inst == 2:
            arg = self._parse_value()
            self.stack.append(arg)
            command = 'push {}'.format(arg)

        elif inst == 3:
            arg = self._parse_address()
            self.reg[arg] = self.stack.pop()
            command = 'pop R{} ({})'.format(arg, self.reg[arg])

        elif inst == 4:
            arg1 = self._parse_address()
            arg2 = self._parse_value()
            arg3 = self._parse_value()
            if arg2 == arg3:
                self.reg[arg1] = 1
            else:
                self.reg[arg1] = 0
            command = 'eq R{} {} {}'.format(arg1, arg2, arg3)

        elif inst == 5:
            arg1 = self._parse_address()
            arg2 = self._parse_value()
            arg3 = self._parse_value()
            if arg2 > arg3:
                self.reg[arg1] = 1
            else:
                self.reg[arg1] = 0
            command = 'gt R{} {} {}'.format(arg1, arg2, arg3)

        elif inst == 6:
            arg = self._parse_value()
            self.reg['addr'] = arg
            command = 'jmp {}'.format(arg)

        elif inst == 7:
            arg1 = self._parse_value()
            arg2 = self._parse_value()
            if arg1 != 0:
                self.reg['addr'] = arg2
            command = 'jt {} {}'.format(arg1, arg2)

        elif inst == 8:
            arg1 = self._parse_value()
            arg2 = self._parse_value()
            if arg1 == 0:
                self.reg['addr'] = arg2
            command = 'jf {} {}'.format(arg1, arg2)

        elif inst == 9:
            arg1 = self._parse_address()
            arg2 = self._parse_value()
            arg3 = self._parse_value()
            self.reg[arg1] = (arg2 + arg3) % 32768
            command = 'add R{} {} {}'.format(arg1, arg2, arg3)

        elif inst == 10:
            arg1 = self._parse_address()
            arg2 = self._parse_value()
            arg3 = self._parse_value()
            self.reg[arg1] = (arg2 * arg3) % 32768
            command = 'mult R{} {} {}'.format(arg1, arg2, arg3)

        elif inst == 11:
            arg1 = self._parse_address()
            arg2 = self._parse_value()
            arg3 = self._parse_value()
            self.reg[arg1] = (arg2 % arg3)
            command = 'mod R{} {} {}'.format(arg1, arg2, arg3)

        elif inst == 12:
            arg1 = self._parse_address()
            arg2 = self._parse_value()
            arg3 = self._parse_value()
            self.reg[arg1] = arg2 & arg3
            command = 'and R{} {} {}'.format(arg1, arg2, arg3)

        elif inst == 13:
            arg1 = self._parse_address()
            arg2 = self._parse_value()
            arg3 = self._parse_value()
            self.reg[arg1] = arg2 | arg3
            command = 'or R{} {} {}'.format(arg1, arg2, arg3)

        elif inst == 14:
            arg1 = self._parse_address()
            arg2 = self._parse_value()
            self.reg[arg1] = 32768 + ~arg2
            command = 'not R{} {}'.format(arg1, arg2)

        elif inst == 15:
            arg1 = self._parse_address()
            arg2 = self._parse_value()
            self.reg[arg1] = self.read_address(arg2)
            command = 'rmem R{} {}'.format(arg1, arg2)

        elif inst == 16:
            arg1 = self._parse_value()
            arg2 = self._parse_value()
            self.cached_memory[arg1] = arg2
            command = 'wmem {} {}'.format(arg1, arg2)

        elif inst == 17:
            arg = self._parse_value()
            command = call_function(arg, self.reg)
            if command == False:
                self.stack.append(self.reg['addr'])
                self.reg['addr'] = arg
                command = 'call {}'.format(arg)

        elif inst == 18:
            if len(self.stack) > 0:
                self.reg['addr'] = self.stack.pop()
                command = 'ret ({})'.format(self.reg['addr'])
            else:
                command = 'stop'

        elif inst == 19:
            arg = self._parse_value()
            sys.stdout.write(chr(arg))
            command = 'out {}'.format(arg)

        elif inst == 20:
            # write_register()
            arg = self._parse_address()
            self.reg[arg] = ord(sys.stdin.read(1))
            command = 'in {} ({})'.format(arg, self.reg[arg])

        elif inst == 21:
            command = 'noop'

        else:
            print 'invalid instruction {}'.format(inst)
            command = 'stop'
        return '- {}: {}'.format(addr, command)



if __name__ == '__main__':
    machine = VM('input/challenge.bin')
    machine.load_state('teleporter')

    while True:
        output = machine.run_next_instruction()
        debug(output)
        if output == 'stop':
            break

