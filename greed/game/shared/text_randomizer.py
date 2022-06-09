import random
from game.casting.power_ups import Power_up
from game.casting.curses import Curses
from game.casting.randomizer import Randomizer

class Text_randomizer(Randomizer):
    
    def __init__(self):
        self._value = 0
        self._power = Power_up()
        self._curse = Curses()
        self._mystery = Randomizer()
        
        

    def renamer(self):
        
        
        name_picker = random.randint(1,5)
        
        #print('the name picker number issssssssssssssssssssssssss.', name_picker) # debugging line
        
        if name_picker == 1:
            name = 'gem'
            self._value = 2
            return name 
        
        elif name_picker == 2:
            name = 'ro'
            self._value = -1
            return name 
            
        elif name_picker == 3:
            name = 'mult'
            self._value = self._power.multiplier()
            return name 
        
        elif name_picker == 4:
            name = 'cur'
            self._value = self._curse.bad_mult()
            return name 
        
        elif name_picker == 5:
            name = 'ran'
            self._value = self._mystery.mystery_box()
            return name 
        
        
    def value_setter(self):
        value = self._value
        
        return value
        
        
        
        
    
