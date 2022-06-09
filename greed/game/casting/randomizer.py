import random
from game.casting.power_ups import Power_up
from game.casting.curses import Curses


class Randomizer (Curses):
    
    def __init__(self):
        self._ran_mult = super().multiplier()
        self._ran_bad = super().bad_mult()
        
    
    def mystery_box(self):
        self._picker = random.randint(1,1000)
        print('the randomizer number picks mystery box nubmerrrrrrrrrrr',self._picker)
        
        
        if self._picker < 200 :
            #print('this is the mult from randomizer here is the value', self._ran_mult)
            return self._ran_mult

        elif self._picker > 800  :
            #print('this is the bad mult from randomizer here is the value', self._ran_bad)
            return self._ran_bad
        
        
        # elif self._picker == 777:
        #     print('Lady Luck Smiles on you.  You win')
        #     return 777
        
        # elif self._picker == 666:
        #     print('OOF, that is what I call BAD LUCK!!!')
        #     bad_luck = -666
        #     return bad_luck
        
        else:
            mystery_points = random.randint(3,10)
            #print('you get mystery points', mystery_points)
            return mystery_points
        
        
        
   