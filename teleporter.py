'''
Python implementation of the teleporter confirmation thing.


Relevant machine code:

R0 and R1 are initialized as 4 and 1.
We want R0 to equal 6 after the function is finished


6027: jt R0 6035        - skip if r0 > 0
6030: add R0 R1 1       - R0 = R1 + 1
6034: ret               - return R0 = R1 + 1; R1 = R1

6035: jt R1 6048        - skip if r1 > 0
6038: add R0 R0 32767   - R0 = R0 - 1
6042: set R1 R7         - R1 = R7
6045: call 6027         - recurse(r0 - 1, r7)
6047: ret               - return recurse(r0 - 1, r7)

6048: push R0

6050: add R1 R1 32767   - R1 = R1 - 1
6054: call 6027         - recurse(r0, r1 - 1)
6056: set R1 R0         - r1 = recurse(r0, r1 - 1)[0]

6059: pop R0

6061: add R0 R0 32767   - r0 = r0 - 1
6065: call 6027         - return recurse(r0 - 1, r1)
6067: ret
'''

'''Initial attempts to write the function in python'''
# def recurse(r0, r1, r7, memo=None):
#     if memo is None:
#         memo = {}
#     if memo.get((r0, r1)) is not None:
#         return memo[(r0, r1)]

#     if r0 == 0:
#         ans = (r1 + 1) % 32768
#     elif r1 == 0:
#         ans = recurse((r0 - 1) % 32768, r7, r7, memo)
#     else:
#         new_r1 = recurse(r0, (r1 - 1) % 32768, r7, memo)
#         ans = recurse((r0 - 1) % 32768, new_r1, r7, memo)
#     memo[(r0, r1)] = ans
#     return ans


'''Optimized version that still takes a long time :( '''
for r7 in range(1, 32768):
    row = range(1, 32769)
    row[-1] = 0
    for r0 in range(1, 5):
        next_row = [row[r7]]
        for r1 in range(1, 32769):
            last = next_row[-1]
            next_row.append(row[last])
        row = next_row
    print '{}: {}'.format(r7, row[1])
    if row[1] == 6:
        break
