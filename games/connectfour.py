#Connect Four for C4 B325 event
#Willow Dennison - wdennison26@cornellcollege.edu
#

import numpy as np
import rich

class Game:
    
    #if either bot is set to none, that slot will be playable in terminal
    #displayGame decides whether to render the game in terminal or to simulate it in the background.
    #do NOT set displayGame to false if you're not using both bots! it's basically impossible to play without seeing the game.
    def __init__(self, displayGame = True, bot1 = None, bot2 = None):
        
        self.displayGame = True
        self.bot1 = bot1
        self.bot2 = bot2

        #turn marker, set to 1 or 2
        self.turn = 1