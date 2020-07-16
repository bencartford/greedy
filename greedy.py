
class Greedy:
    def __init__(self, num_dice):
        assert (num_dice == 5)
        return

    def value(self, roll):
        """
        Based on the game's definition, value and group the dice. 
        This will return a list of all the possible ways to number them. 
        ASSUMPTIONS:
        12345 --  1000pts
        23456 --  1000pts
        111   --  1000pts
        666   --   900pts
        nnn   --   n00pts (for remaining)
        1     --   100pts
        5     --    50pts

        values are returned in tuples of (VALUE, REMAINING DICE)
        """
        values = []
        if all(map(lambda x: x==1, roll[:5])) or all(map(lambda x: x==1, roll[1:])):
            ### These are rolls with all consecutive numbers
            values.append([1000, 0])
        
        for num in range(6):
            # Look for triples
            if roll[num] >= 3:
                copy_roll = roll
                if num == 0: # At least 3 1's
                    values.append([1000, 2])
                    copy_roll[0] -= 3
                    new_val = [1000, 2]

                    # If there's other 1's remaining
                    if copy_roll[0] > 0:
                        new_val[0] += (copy_roll[0]*100)
                        new_val[1] -= copy_roll[0]
                    
                    # A dice roll of 5
                    if copy_roll[4] > 0: 
                        new_val[0] += (copy_roll[4]*50)
                        new_val[1] -= copy_roll[4]
                    values.append(new_val)

                elif num == 5:
                    values.append([900, 2])
                    copy_roll[5] -= 3
                    new_val = [900, 2]

                    # Any 1's?
                    if copy_roll[0] > 0:
                        new_val[0] += (copy_roll[0]*100)
                        new_val[1] -= copy_roll[0]
                    
                    # If there're any 5's remaining
                    if copy_roll[4] > 0: 
                        new_val[0] += (copy_roll[4]*50)
                        new_val[1] -= copy_roll[4]
                    values.append(new_val)
                
                else:
                    # We need to add 1 to the index since index 0 == 1 on dice, ind 1 == 2 on dice
                    values.append([(num+1)*100, 2])
                    copy_roll[num] -= 3
                    new_val = [(num+1)*100, 2]

                    # Any 1's?
                    if copy_roll[0] > 0:
                        new_val[0] += (copy_roll[0]*100)
                        new_val[1] -= copy_roll[0]
                    
                    # Any 5's?
                    if copy_roll[4] > 0: 
                        new_val[0] += (copy_roll[4]*50)
                        new_val[1] -= copy_roll[4]
                    values.append(new_val)

        for one in range(roll[0]+1):
            for five in range(roll[4]+1):
                if one+five > 0:
                    values.append([(one*100)+(five*50), sum(roll)-one-five])
        
        # If you use all the dice, you get a fresh roll
        for v in range(len(values)):
            if values[v][1]==0:
                values[v][1] = 5
                
        return values