#Connect Four for C4 B325 event
#Willow Dennison - wdennison26@cornellcollege.edu
#

import numpy as np
import rich
from queue import Queue

#holds the bot players and all info for the game, actually simulates the game
class Game:
    

    #if either bot is set to none, that slot will be playable in terminal
    #displayGame decides whether to render the game in terminal or to simulate it in the background.
    #do NOT set displayGame to false if you're not using both bots! it's basically impossible to play without seeing the game.
    def __init__(self, displayGame: bool = True, bot1 = None, bot2 = None):
        
        self.displayGame = True
        self.bot1 = bot1
        self.bot2 = bot2

        #turn marker, set to 1 or 2
        self.turn = 1

        self.gameState = GameState()



#wrapper for a 6x7 array to store the state of the board
class GameState:


    def __init__(self):
        
        self.board = np.zeros((6, 7))
        print(self.board)
        self.placeToken(1, 1)


    #how to handle placing in full column?
    def placeToken(self, playerNum: int, col: int):
        
        placed = False

        #count backwards :3
        for i in range(-1, -7, -1):
            if self.board[i][col] == 0:
                print(col, i)
                self.board[i][col] = playerNum
                placed = True
                print(self.board)
                break

        if not placed:
            raise Exception("u fucked up dawg")

        self.winCheck()


    #check if anyone has 4 in a row, return 0 (no winner), 1 (player 1 wins) or 2 (player 2 wins)
    #check runs every move, so no risk of conflicting results
    def winCheck(self):
        
        #check horizontals
        for row in self.board:
            for i in range(4):
                if list(row[i:i+4]) in ([1,1,1,1], [2,2,2,2]):
                    return row[i]
        
        #check verticals
        rotatedBoard = np.rot90(self.board, axes = (0,1))
        for col in rotatedBoard:
            for i in range(3):
                if list(col[1:i+4]) in ([1,1,1,1], [2,2,2,2]):
                    return col[i]
                
        #check diagonals
        for i in range(3):
            for j in range(4):
                diag = [self.board[i][j],
                        self.board[i+1][j+1],
                        self.board[i+2][j+2],
                        self.board[i+3][j+3]]
                if diag in ([1,1,1,1], [2,2,2,2]):
                    return diag[0]

        flippedBoard = np.flip(self.board)
        for i in range(3):
            for j in range(4):
                diag = [flippedBoard[i][j],
                        flippedBoard[i+1][j+1],
                        flippedBoard[i+2][j+2],
                        flippedBoard[i+3][j+3]]
                if diag in ([1,1,1,1], [2,2,2,2]):
                    return diag[0]
        


Game()