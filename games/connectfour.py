#Connect Four for C4 B325 event
#Willow Dennison - wdennison26@cornellcollege.edu

import numpy as np
from rich import print

#holds the bot players and all info for the game, actually simulates the game
class Game:
    

    #if either bot is set to none, that slot will be playable in terminal
    #displayGame decides whether to render the game in terminal or to simulate it in the background.
    #do NOT set displayGame to false if you're not using both bots! it's basically impossible to play without seeing the game.
    def __init__(self, displayGame: bool = True, bot1 = None, bot2 = None):
        
        self.displayGame = displayGame
        self.bot1 = bot1
        self.bot2 = bot2

        #turn marker, set to 1 or 2
        self.turn = 1

        self.gameState = GameState()

    
    #simulate the next player's turn and augment the turn counter
    def nextTurn(self):

        match self.turn:

            case 1:
                if self.bot1:
                    #passes bots a 6x7 array of the board state with 0 for empty, 1 for player 1, 2 for player 2
                    #expects a single int [0, 6] for the column to place their next token in
                    col = self.bot1.think(self.gameState.board)
                    self.gameState.placeToken(self.turn, col)
                    self.turn = 2

                else:
                    col = int(input(f'Player {self.turn}: Please enter a number between 1 and 7 for which column to place your token in. '))
                    self.gameState.placeToken(self.turn, col - 1)
                    self.turn = 2

            case 2:
                if self.bot2:
                    col = self.bot2.think(self.gameState.board)
                    self.gameState.placeToken(self.turn, col)
                    self.turn = 1

                else:
                    col = int(input(f'Player {self.turn}: Please enter a number between 1 and 7 for which column to place your token in. '))
                    self.gameState.placeToken(self.turn, col - 1)
                    self.turn = 1
                  
        if self.gameState.winState > 0:
            self.playing = False


    #neatly display the game board
    def printBoard(self):
        
        board = self.gameState.board

        for row in board:
            for tile in row:
                match tile:
                    case 0:
                        fancyTile = '[black]0[/black]'
                    case 1:
                        fancyTile = '[bold red]0[/bold red]'
                    case 2:
                        fancyTile = '[bold blue]0[/bold blue]'
                
                print('|', end = '')
                print(fancyTile, end = '')
            
            #end line
            print('|')
         
        #print(self.gameState.board)


    #actually run the game
    def play(self):

        #set flag for to be triggered when a player wins
        self.playing = True

        while self.playing:

            if self.displayGame:
                self.printBoard()

            self.nextTurn()
        
        #should only return when the value is 1 or 2
        self.printBoard()
        print(f'Congratulations, Player {int(self.gameState.winState)}')
        return self.gameState.winState



#wrapper for a 6x7 array to store the state of the board
class GameState:


    def __init__(self):
        
        self.board = np.zeros((6, 7))

        #tracks if a player has won, sets to 1 if player 1 wins, 2 if player 2 wins
        self.winState = 0

    #how to handle placing in full column?
    def placeToken(self, playerNum: int, col: int):
        
        placed = False

        #count backwards :3
        for i in range(-1, -7, -1):

            if self.board[i][col] == 0:
                self.board[i][col] = playerNum

                placed = True
                break

        if not placed:
            raise Exception('u fucked up dawg')

        self.winState = self.winCheck()


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
                if list(col[i:i+4]) in ([1,1,1,1], [2,2,2,2]):
                    return col[i]
                
        #check diagonals
        for i in range(3):
            for j in range(4):
                diag = [int(self.board[i][j]),
                        int(self.board[i+1][j+1]),
                        int(self.board[i+2][j+2]),
                        int(self.board[i+3][j+3])]
                if diag in ([1,1,1,1], [2,2,2,2]):
                    return diag[0]

        flippedBoard = np.flip(self.board, (1,))
        for i in range(3):
            for j in range(4):
                diag = [int(flippedBoard[i][j]),
                        int(flippedBoard[i+1][j+1]),
                        int(flippedBoard[i+2][j+2]),
                        int(flippedBoard[i+3][j+3])]
                if diag in ([1,1,1,1], [2,2,2,2]):
                    return diag[0]
                
        #if no winner yet:
        return 0
        


Game().play()