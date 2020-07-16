from greedy import Greedy
from dice import roll_dice
import time

NUM_DICE = 5
WINNING_POINTS = 8000

class Strategy:
    def __init__(self, name=''):
        self.name = name
        self.points = 0
        return
    def decision(self, roll, current_value):
        return {'keep': [], 'return': []}

    def __str__(self):
        return self.name

class RealBasic(Strategy):
    # Get over some threshold then take that value
    def __init__(self, cutoff):
        super().__init__(name='<{}'.format(cutoff))
        self.cutoff = cutoff
    
    def decision(self, values, current_value):
        best_choice = [0, 0]
        for choice in values:
            if choice[0] > best_choice[0]:
                best_choice = choice
        if best_choice[0] + current_value > self.cutoff:
            best_choice[1] = None 
            # ^ Done with this turn
        return best_choice

class DiceBasic(Strategy):
    # Get over some threshold then take that value
    def __init__(self, num_dice):
        super().__init__(name='<{}'.format(num_dice))
        self.n_dice = num_dice
    
    def decision(self, values, current_value):
        best_choice = [0, 0]
        best_nodice = [0,None]
        for choice in values:
            if choice[0] > best_choice[0] and choice[1] > self.n_dice:
                best_choice = choice
            elif choice[0] > best_nodice[0]:
                best_nodice[0] = choice[0]
        if best_choice[0] == 0: # Never updated
            return best_nodice

        return best_choice


### We'll make some basic strategies

if __name__=="__main__":
    gd = Greedy(num_dice=NUM_DICE)
    al500 = DiceBasic(2)
    al250 = RealBasic(200)
    best_game = ['', 1000]
    best_values = []

    wins = {al500.name: 0, al250.name: 0}
    num_turns = 0
    for game_num in range(50000):
        print("GAMES :: {}".format(wins), end='\r')
        current_points = {al500.name: 0, al250.name: 0}
        has_won = False
        this_game = 0
        these_values1 = []
        these_values2 = []
        
        while not has_won:
            num_turns += 1
            this_game += 1
            if current_points[al250.name] >= WINNING_POINTS:
                wins[al250.name] += 1
                if this_game < best_game[1]:
                    best_game = [al250.name, this_game]
                    best_values = these_values1
                has_won = True
            if current_points[al500.name] >= WINNING_POINTS:
                wins[al500.name] += 1
                if this_game < best_game[1]:
                    best_game = [al500.name, this_game]
                    best_values = these_values2
                has_won = True

            num_dice = NUM_DICE
            turn1 = True
            pts1 = 0
            while turn1:
                rroll = roll_dice(num_dice)
                vals = gd.value(rroll)
                if len(vals) == 0:  # No Points!
                    turn1 = False
                    pts1 = 0
                    
                
                else:
                    choice = al250.decision(vals, pts1)
                    these_values1.append(choice)
                    if choice[1] == None:  # Decided to take points
                        current_points[al250.name] += choice[0] + pts1
                        turn1 = False
                    else:
                        pts1 += choice[0]
                        num_dice = choice[1]

            num_dice = NUM_DICE
            turn2 = True
            pts2 = 0
            while turn2:
                rroll = roll_dice(num_dice)
                vals = gd.value(rroll)
                if len(vals) == 0:  # No Points!
                    turn2 = False
                    pts2 = 0
                
                else:
                    choice = al500.decision(vals, pts2)
                    these_values2.append(choice)
                    if choice[1] == None:  # Decided to take points
                        current_points[al500.name] += choice[0] + pts2
                        turn2 = False
                        
                    else:
                        pts2 += choice[0]
                        num_dice = choice[1]

            

    print("\nWINS :: {}".format(wins))
    print("AVG ROLLS/GAME :: {}".format(num_turns/50000))
    print("BEST GAME :: {}".format(best_game))
    print("BEST SEQUENCE :: {}".format(best_values))


