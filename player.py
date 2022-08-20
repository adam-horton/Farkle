from dice import Die
import numpy as np

class Player:

    def __init__(self):
        self._dice = []
        for x in range(5):
            self._dice.append(Die())
        self._counts = [0 for x in range(6)]

    def _update_counts(self):
        self._counts = [0 for x in range(6)]
        for die in self._dice:
            if not die.is_locked():
                self._counts[die.get_value() - 1] += 1
        return self._counts  

    def all_dice_locked(self):
        all_locked = True
        for die in self._dice:
            if not die.is_locked():
                all_locked = False
        
        return all_locked

    def count_locked(self):
        count = 0
        for die in self._dice:
            if die.is_locked():
                count += 1
        return count

    def roll(self):
        for die in self._dice:
            if not die.is_locked():
                die.roll()
        self._update_counts()

    def show_all(self):
        locked = ""
        unlocked = ""
        for die in self._dice:
            if die.is_locked():
                locked += str(die.get_value()) + " "
            else:
                unlocked += str(die.get_value()) + " "
        
        print(locked + "| " + unlocked)

    def unlock_all(self):
        for die in self._dice:
            die.unlock()
        self._update_counts()

    def lock(self, subset):
        if subset == None or subset == []:
            return 0
        for x in subset:
            self._dice[x].lock()
        self._update_counts()

        if len(subset) == 5:
            return 1000
        elif len(subset) == 3:
            if self._dice[subset[0]].get_value() == 1:
                return 1000
            else:
                return 100 * self._dice[subset[0]].get_value()
        elif self._dice[subset[0]].get_value() == 1:
            return 100 * len(subset)
        elif self._dice[subset[0]].get_value() == 5:
            return 50 * len(subset)
    
    def find_triples(self):
        triple_val = -1
        for position in range(len(self._counts)):
            if self._counts[position] >= 3:
                triple_val = position + 1
                break
        
        if triple_val == -1:
            return None
        
        triple_list = []
        for position in range(len(self._dice)):
            die = self._dice[position]
            if not die.is_locked() and die.get_value() == triple_val:
                triple_list.append(position)
            if len(triple_list) == 3:
                break
        
        return triple_list

    def find_straight(self):
        if self._counts == [1, 1, 1, 1, 1, 0] or self._counts == [0, 1, 1, 1, 1, 1]:
            return [x for x in range(5)]
        else:
            return None

    def find_ones(self):
        if self._counts[0] == 0:
            return None
        
        one_list = []
        for position in range(len(self._dice)):
            die = self._dice[position]
            if not die.is_locked() and die.get_value() == 1:
                one_list.append(position)

        return one_list

    def find_fives(self):
        if self._counts[4] == 0:
            return None
        
        five_list = []
        for position in range(len(self._dice)):
            die = self._dice[position]
            if not die.is_locked() and die.get_value() == 5:
                five_list.append(position)

        return five_list

    def check_farkle(self):
        if (    
            self.find_straight() == None and
            self.find_triples() == None and
            self.find_ones() == None and
            self.find_fives() == None
            ):
            return True
        else:
            return False

class Info(object):
    def __init__(self):
        self.sum = 0
        self.num_events = 0

    def add_event(self, score):
        self.num_events += 1
        self.sum += score

    def __str__(self):
        if self.num_events == 0:
            return '(0, 0)'
        return '(' + str(round(self.sum/self.num_events, 3)) +  ', ' + str(self.num_events) + ')'

def roll_once(num):
    bob = Player()

    bob.lock([x for x in range(5 - num)])

    bob.roll()

    sum = 0

    if bob.find_straight() != None:
        sum += 1000
        return sum, 0
    sum += bob.lock(bob.find_triples())
    sum += bob.lock(bob.find_ones())
    sum += bob.lock(bob.find_fives())

    dice_left = 5 - bob.count_locked()

    return sum, dice_left

def pretty_print(array):
    for row in array:
        print(*row)

def generate_table():
    info_array = [[Info() for x in range(5)] for y in range(6)]

    for y in range(5):
        for x in range(10000000):
            (points, dice_left) = roll_once(y+1)
            info_array[dice_left][y].add_event(points)

    pretty_print(info_array)

def calculate():
    p10 = 0.3333333333
    p11 = 0.6666666667
    p20 = 0.1111111111
    p21 = 0.4444444444
    p22 = 0.4444444444
    p30 = 0.0556
    p31 = 0.222
    p32 = 0.444
    p33 = 0.278
    p40 = 0.0371
    p41 = 0.140
    p42 = 0.296
    p43 = 0.370
    p44 = 0.157
    p50 = 0.0555
    p51 = 0.108
    p52 = 0.219
    p53 = 0.293
    p54 = 0.246
    p55 = 0.0771

    v10 = 75
    v11 = 0
    v20 = 150
    v21 = 75
    v22 = 0
    v30 = 364
    v31 = 150
    v32 = 75
    v33 = 0
    v40 = 509
    v41 = 361
    v42 = 150
    v43 = 75
    v44 = 0
    v50 = 817
    v51 = 518
    v52 = 361
    v53 = 150
    v54 = 75
    v55 = 0

    ev1 = p10 * v10
    ev2 = (p21 * (v21 + ev1)) + (p20 * v20)
    ev3 = (p32 * (v32 + ev2)) + (p31 * (v31 + ev1)) + (p30 * v30)
    ev4 = (p43 * (v43 + ev3)) + (p42 * (v42 + ev2)) + (p41 * (v41 + ev1)) + (p40 * v40)
    numerator = (p54 * (v54 + ev4)) + (p53 * (v53 + ev3)) + (p52 * (v52 + ev2)) + (p51 * (v51 + ev1)) + (p50 * v50)
    line2 = (p52 * p21 * p10) + (p52 * p20)
    line3 = (p53 * p32 * p21 * p10) + (p53 * p32 * p20) + (p53 * p31 * p10) + (p53 * p30)
    line4 = (p54 * p43 * p32 * p21 * p10) + (p54 * p43 * p32 * p20) + (p54 * p43 * p31 * p10) + (p54 * p43 * p30) + (p54 * p42 * p21 * p10) + (p54 * p42 * p20) + (p54 * p41 * p10) + (p54 * p40)

    denominator = 1 - (p50 + (p51 * p10) + line2 + line3 + line4)
    
    real_value_5 = numerator / denominator
    real_value_1 = (p10 * (v10 + real_value_5))
    real_value_2 = (p21 * (v21 + real_value_1)) + (p20 * (v20 + real_value_5))
    real_value_3 = (p32 * (v32 + real_value_2)) + (p31 * (v31 + real_value_1)) + (p30 * (v30 + real_value_5))
    real_value_4 = (p43 * (v43 + real_value_3)) + (p42 * (v42 + real_value_2)) + (p41 * (v41 + real_value_1)) + (p40 * (v40 + real_value_5))

    return [real_value_1, real_value_2, real_value_3, real_value_4, real_value_5]

    
    
if __name__ == "__main__":
    print(calculate())