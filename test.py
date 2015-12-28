from itertools import permutations

# red = 2
# blue = 9
# concave = 7
# shiny = 5
# corroded = 3

coins = [2, 9, 7, 5, 3]

for combo in permutations(coins):
    exec("ans = {} + {} * {} ** 2 + {} ** 3 - {}".format(*combo))
    if ans == 399:
        print combo
