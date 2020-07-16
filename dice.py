from random import randint

def roll_dice(num_dice):
    rolled = [0,0,0,0,0,0]
    for i in range(num_dice):
        rolled[randint(0, 5)] += 1
    return rolled

