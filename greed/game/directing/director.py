from game.shared.point import Point
from game.shared.text_randomizer import Text_randomizer
from game.casting.curses import Curses
from game.casting.randomizer import Randomizer
from game.casting.falling_object import FallingObject
import random

class Director:
    """A person who directs the game. 
    
    The responsibility of a Director is to control the sequence of play.

    Attributes:
        _keyboard_service (KeyboardService): For getting directional input.
        _video_service (VideoService): For providing video output.
    """

    def __init__(self, keyboard_service, video_service, collection, power_up):
        """Constructs a new Director using the specified keyboard and video services.
        
        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
            video_service (VideoService): An instance of VideoService.
            collection (collection): The collection of actors.
            power_up (PowerUp): the increasing value
        
        Attributes:
            _floor(int): This is the floor where the player stands and the falling objects should be gone when touch
            _points: This is the current points of the player
            _curses (Curses): decreasing value to points
        """
        self._keyboard_service = keyboard_service
        self._video_service = video_service
        self._floor = 580
        self._collection = collection
        self._points = 0
        self._power_up = power_up
        self._curses = Curses()
        self._randomizer = Randomizer()
        self._rando_text = Text_randomizer()
        #self._amp = 0
        
        self._falling_object = FallingObject()
        
    def start_game(self):
        """Starts the game using the given collection. Runs the main game loop.
        """
        self._video_service.open_window()
        while self._video_service.is_window_open():
            self._get_inputs(self._collection)
            self._do_updates(self._collection)
            self._do_outputs(self._collection)
        self._video_service.close_window()

    def _get_inputs(self, collection):
        """Gets directional input from the keyboard and applies it to the player.
        
        Args:
            collection (collection): The collection of actors.
        """
        player = collection.get_first_game_object("players")
        velocity = self._keyboard_service.get_direction() #this sets an x,y corridnate
        player.set_velocity(velocity)

    def _do_updates(self, collection):
        """Updates the player's position and resolves any collisions with falling_objects.
        
        Args:
            collection (collection): The collection of actors.
        """
        rename = self._rando_text
        mystery = self._randomizer
        banner = collection.get_first_game_object("banners")
        player = collection.get_first_game_object("players")
        falling_objects = collection.get_game_objects("falling_objects")
        
        #print('your points are', self._points)
        banner.set_text(f"Score: {self._points: .0f}")
        max_x = self._video_service.get_width()
        max_y = self._video_service.get_height()
        player.move_next(max_x , max_y)  
        
        for falling_object in falling_objects:
            if player.distance(falling_object.get_position()) < 20: #collision detection
                #this is if the player gets a multiplier power up
                if falling_object.get_text() == "m":
                    #print('you got a mult, points before multttttttttttttttttttttttttttttttttttttt',self._points)
                    #mult = (self._points * self._power_up.multiplier())#falling_object.get_points()) 
                    self._points *= (falling_object.get_points() + self._power_up.multiplier()) 
                    #print('points after mult',self._points)
                    #collection.remove_game_object("falling_objects", falling_object)
                    
                #if player gets a curse    
                elif falling_object.get_text() == 'c':
                    #print('points before curseeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',self._points)
                    curse = (self._points *  self._curses.bad_mult()) 
                    self._points += curse
                    #print('points after curse',self._points)
                    #collection.remove_game_object('falling_objects', falling_object)
  
                #if player gets a randomizer item    
                elif falling_object.get_text() == 'r':
                    #print('points before randomizerrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr',self._points)
                    result = mystery.mystery_box()
                    print('this is the outcome of the mystery box', result)
                    
                    
                    if result > 2: #this is if the mystery box just give a flat number increase
                        print('points before flat mystery box',self._points)
                        self._points += result
                        print('points after randomizer',self._points)
                        #collection.remove_game_object('falling_objects', falling_object)
                    
                    elif result > 0 and result <= 2: #if mystery box give a positive multiplier
                        print('this is a randomizer multiplier',result)
                        print('points before good mystery box',self._points)
                        self._points += (self._points * result)
                        print('points after good mystery box',self._points)
                        #collection.remove_game_object('falling_objects', falling_object)
                        
                    elif result < 0:
                        print('this is a negative multiplier from mystery box')
                        print('points before bad mystery', self._points)
                        self._points += (self._points * result)
                        # ran = (self._points * self._randomizer.mystery_box())
                        #   self._points += ran
                        print('points after randomizer',self._points)
                        #collection.remove_game_object('falling_objects', falling_object)
                
                # can add future power ups here

                #if player gets a rock
                elif falling_object.get_text() == 'O':
                    # print('you hit a rock')
                    # print('points before rock', self._points)
                    self._points += falling_object.get_points()
                    #print('points after rock', self._points)
                    #collection.remove_game_object('falling_objects', falling_object)
                    
                # if not a power up, curse, or rock it is a gem
                else:
                    #print('you got a gemmmmmmmmmmmmm your old points',self._points)
                    self._points += falling_object.get_points()
                    #print('your points are nowwwwwwwwwwwwww',self._points)
                    #collection.remove_game_object('falling_objects', falling_object)

        #falling objects
        for falling_object in falling_objects: 
            velocity = Point(0,(random.randint(8,15)))# + self._amp )) # this will make the gems and rocks fall faster.  If the number is below zero it will go in reverse
            falling_object.set_velocity(velocity) 
            falling_object.move_next(max_x, max_y)
            
            
        # going through all the falling objects and if falling_object falls past floor...
        # then it will get renamed, its value reset, starting position x coordinate randomized and y coordinate starting at the top of the screen.  
        # After that it is again put into the list of falling objects
        for falling_object in falling_objects:
            #print(falling_object.get_position().get_y()) #this will get the y point debugging line
            if falling_object.get_position().get_y() > self._floor:
                #print('y is greater than the floor') # debugging
                #print('old name for the object is.............', falling_object.get_text())
                falling_object.set_text(rename.renamer())
               # print('the new name is ', falling_object.get_text())
                #print('here is the old value',falling_object.get_points())
                falling_object.set_points(rename.value_setter())
                #print('this is the new value',falling_object.get_points())
                newx = random.randint(1,max_x)
                newy = max_y
                repost = Point(newx,newy)
                falling_object.set_position(repost)
                #print('new object incomingggggggggggggggggggggggggggg') # debugging
                collection.add_game_object('falling_objects', falling_object)
                #print('the new name for the object is.........',falling_object.get_text()) #debugging 
        
        # if self._points >= 10:
        #     banner.set_text("You Win")

    def _do_outputs(self, collection):
        """Draws the actors on the screen.
        
        Args:
            collection (collection): The collection of actors.
        """
        self._video_service.clear_buffer()
        actors = collection.get_all_game_objects()
        self._video_service.draw_game_objects(actors)
        self._video_service.flush_buffer()
        