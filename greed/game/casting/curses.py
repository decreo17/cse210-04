import random
from game.casting.power_ups import Power_up


class Curses(Power_up):
    
    def bad_mult(self): 
        mult = super().multiplier()
        bad = (mult * - 1)
        print('this is curses class bad_mult method being activated.  The bad mult is', bad)
        
        return bad