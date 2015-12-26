from itertools import permutations

# red = 2
# blue = 9
# concave = 7
# shiny = 5
# corroded = 3

9 2 5 7 3

coins = [2, 9, 7, 5, 3]

for combo in permutations(coins):
    exec("ans = {} + {} * {} ** 2 + {} ** 3 - {}".format(*combo))
    if ans == 399:
        print combo


# 0 25975
# 1 25974
# 2 26006
# 3 0
# 4 101
# addr 1799
# 6 0
# 7 0
# 5 0
