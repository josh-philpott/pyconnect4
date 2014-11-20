import pygame
import sys
import copy 
import random

global_computer = 2
global_human = 1


class ConnectFourHelper:
    """ConnectFourHelper contains helper functions for ConnectFourGame """

    def __init__(self):
        pass
    
    def maxValidScoreIndex(self, scores, valid):
        max_n = -100000
        best_moves = []

        for i in range(0,len(scores)):
            if valid[i]==True:
                if scores[i] > max_n:
                    best_moves = []
                    max_n = scores[i]
                    best_moves.append(i)
                elif scores[i] == max_n:
                    best_moves.append(i)
        return random.choice(best_moves), max_n
    
    def minValidScoreIndex(self, scores, valid):
            min_n = 100000
            best_moves = []

            for i in range(0,len(scores)):
                if valid[i]==True:
                    if scores[i] < min_n:
                        best_moves = []
                        min_n = scores[i]
                        best_moves.append(i)
                    elif scores[i] == min_n:
                        best_moves.append(i)
            return random.choice(best_moves), min_n

    def minimax(self, board, player, depth, maxDepth=100,alpha=-1000, beta=1000):
        """ recursive minimax algorithm returns best move for player
        from given board state. 
        
        Keyword arguments:
        board  -- 6x7 2D list representing board state
        player -- player to determine optimal move for
        depth  -- current search depth
        maxDepth -- maxDepth to explore to
        
        if there are multiple equivalent "best moves",
        will return a random element from a set of best moves
        """
        #if game is over or depth is maxed out, return current board score
        if self.isGameOver(board):
            return 0, self.getScore(board,global_computer)
        if depth==maxDepth:
            return 0, self.getScore(board,global_computer)
        
        scores=[]
        moves =[]
        min_score_index = 0
        max_score_index = 0
        
        if player==1:
            opponent=2
        if player==2:
            opponent=1
        
        #Populate score array by doing each potential move
        isValid=[]
        
        #First see if there are any winning moves and take them
        if player==1 and depth==0:
            for i in range(0,7):
                potential_board = copy.deepcopy(board)
                #if move is valid, run minimax on substates
                if self.isMoveValid(potential_board,i):
                    isValid.append(True)
                    self.dropPiece(i,global_computer,potential_board)   
                    if self.checkWinner(potential_board)==global_computer:
                        print "Winning Move!"
                        return i, 100
        
        for i in range(0,7):
            potential_board = copy.deepcopy(board)
            #if move is valid, run minimax on substates
            if self.isMoveValid(potential_board,i):
                isValid.append(True)
                if(player==1):
                    self.dropPiece(i,global_computer,potential_board)
                else:
                    self.dropPiece(i,global_human,potential_board)
                    
                #Keep it from not taking winning move
                if depth==0 and self.checkWinner(potential_board)==player:
                    return i, 100
                score=(self.minimax(potential_board, opponent,depth+1, maxDepth)[1])
                scores.append(score)
                if(player==1):
                    if(score>alpha):
                        alpha = score
                if(player==2):
                    if(score<beta):
                        beta = score
                if(alpha>=beta):
                    break
            else:
                isValid.append(False)
                scores.append(0)
                
        if depth==0:
            print scores
            
        max_score_index, max_score = self.maxValidScoreIndex(scores, isValid)
        min_score_index, min_score = self.minValidScoreIndex(scores, isValid)

        #get moves that are "equivalent" to best move
        #and return 
        if player == 1:            
            return max_score_index, max_score
        else:
            return min_score_index, min_score+depth
        

    def isMoveValid(self, board, col=None):
        """Determines if a move is valid
        
        if col is set to integer,
        Returns True if col is valid move, False if invalid
        
        if col is set to None,
        Returns True if board is not full, False if it is full
        """
        
        
        if col==None:
            for i in range(0,7):
                if board[0][i]==0:
                    return True
            return False
        else:
            if board[0][col]==0:
                return True
            return False   
    def isGameOver(self, board):
        """Returns true if there are no possible moves OR there is a winner"""
        if(self.isMoveValid(board)==True and not self.checkWinner(board)):
            return False
        else:
            return True

    def getScore(self, board, player):
        """Return game score based off of win state"""
        if player==1:
            computer = 2
        else:
            computer = 1
    
        
        if self.checkWinner(board)==player:
            return 100
        elif self.checkWinner(board)==computer:
            return -100
        else:
            return 0
        

    def checkWinner(self, board):
        """Returns winner. Check for all possible winning combinations"""

        #Check for winner horizontal
        for row in range (0,6):
            for start in range (0,4):
                if board[row][start]!=0:
                    if (board[row][start] == board[row][start+1] ==
                        board[row][start+2] == board[row][start+3]):
                        return board[row][start]

        #Check for winner diagn - bottom-left to top-right
        for row in range (0,3):
            for start in range (0,4):
                if board[row][start]!=0:
                    if (board[row][start] == board[row+1][start+1] ==
                        board[row+2][start+2] == board[row+3][start+3]):
                        return board[row][start]

        #Check for winner diagn - top-left to bottom-right
        for row in range (3,6):
            for start in range (0,4):
                if board[row][start]!=0:
                    if (board[row][start] == board[row-1][start+1] ==
                        board[row-2][start+2] == board[row-3][start+3]):
                        return board[row][start]

        #Check for winner vertical
        for row in range (0,3):
            for start in range (0,7):
                if board[row][start]!=0:
                    if (board[row][start] == board[row+1][start] ==
                        board[row+2][start] == board[row+3][start]):
                        return board[row][start]		

    def getPossibleBoards(self, player, board):
        """Returns list of possible boards"""
        board_states = []

        for col in range(0,7):
            for row in range(5,-1,-1):
                temp_board = []
                if board[row][col]==0:
                    temp_board = copy.deepcopy(board)
                    temp_board[row][col]=player
                    board_states.append(temp_board)
                    break
        return board_states

    def dropPiece(self, col, player, board):
        """ Make move on current board. """

        for i in range(5,-1,-1):
            if board[i][col]==0:
                board[i][col]=player
                return
        return



class ConnectFourGame:
    """Class responsible for handling an instance of a connect four game
    Requires helper class ConnectFourHelper
    """

    helper = ConnectFourHelper()

    def __init__(self, player=1):
        self.board = [[0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0]] 
        if player>2 or player < 1:
            self.player = 1
        else:
            self.player = player

        if self.player==1:
            self.computer=2
        else:
            self.computer=1


    def dropPiece(self, col, player):
        """ Applys move to game board. Returns 1 if valid, 0 if invalid """

        isMoveValid = self.helper.isMoveValid(self.board, col)

        if isMoveValid:
            self.helper.dropPiece(col, player, self.board)
            return 1
        else:
            return 0

    def getBoard(self):
        """Returns list representing game board"""
        return self.board

    def getWinner(self):
        """Returns winner if one 	exists. Otherwise, returns 0"""
        return self.helper.checkWinner(self.board)

    def makeComputerMove(self):
        """Simulates computer move using minimax algorithm"""
        move, score = self.helper.minimax(self.board, 1, 0, maxDepth=4)
        
        print "Moving to",move,"with a score of",score
        self.dropPiece(move, global_computer)
        
class GUI:
    def __init__(self):
        pygame.init()

        #handle screen
        self.size = width, height = 900,800
        self.margin_top  = 100
        self.margin_left = 100
        self.screen = pygame.display.set_mode(self.size)
        
        pygame.display.set_caption("Connect Four")

        #Images
        self.black_token = pygame.image.load("images/black.png")
        self.red_token = pygame.image.load("images/red.png")
        self.grid_tile = pygame.image.load("images/board.png")

    def clearScreen(self):
        """Clear screen by filling with white"""
        white = 255,255,255
        self.screen.fill(white)

    def drawBoard(self,board):
        """ Draws the grid using grid_tile """
        for i in range(0, 6):
            for j in range(0, 7):
                if board[i][j]==0:
                    self.screen.blit(self.grid_tile,((j+1)*self.margin_left,
                                                     (i+1)*self.margin_top))
                elif board[i][j]==1:
                    self.screen.blit(self.red_token,((j+1)*self.margin_left,
                                                     (i+1)*self.margin_top))
                elif board[i][j]==2:
                    self.screen.blit(self.black_token,((j+1)*self.margin_left,
                                                       (i+1)*self.margin_top))

        for row in range(100, 800, 100):
            for column in range(100, 700, 100):
                self.screen.blit(self.grid_tile, (row, column))

    def drawTokens(self,move):
        """Draws player tokens to screen"""
        for i in range(0,7):
            if move[i]==1:
                self.screen.blit(self.red_token, ((((i+1)*100)), 0))
            if move[i]==2:
                self.screen.blit(self.black_token, ((((i+1)*100)), 0))
    def drawGame(self, board, player_move, optional=0):
        self.clearScreen()
        self.drawTokens(player_move)
        self.drawBoard(board)
        pygame.display.update()        
        

    def getPlayerMove(self,player,board):
        """Returns index of player move selection"""

        player_move = [0,0,0,player,0,0,0]

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key==pygame.K_LEFT:
                        player_move.append(player_move.pop(0))
                    elif event.key==pygame.K_RIGHT:
                        player_move.insert(0, player_move.pop())
                    elif event.key==pygame.K_RETURN:
                        return player_move.index(player)
            self.drawGame(board,player_move,1)
            
    def drawWinner(self, winner, board):
        self.clearScreen()
        self.drawBoard(board)   
        myfont = pygame.font.SysFont("Arial", 30)

        label = myfont.render("Player " + str(winner) + " won!", 1, (0,0,0))
        self.screen.blit(label,(370,10))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                sys.exit()        
        
        
            



player = global_human
gui = GUI()
game = ConnectFourGame(player)

while True: 
    if player==1:
        #get player move first
        while True:
            move = gui.getPlayerMove(1, game.getBoard())
            if game.dropPiece(move,1)==1:
                break
        gui.drawGame(game.getBoard(), [0,0,0,0,0,0,0], optional=0)
        if game.getWinner():
            break
        game.makeComputerMove()
        gui.drawGame(game.getBoard(), [0,0,0,0,0,0,0], optional=0)
        if game.getWinner():
            break        

    else:
        game.makeComputerMove()
        gui.drawGame(game.getBoard(), [0,0,0,0,0,0,0], optional=0)
        if game.getWinner():
                    break         
        while True:
            move = gui.getPlayerMove(2, game.getBoard())
            if game.dropPiece(move,2)==1:
                break
        gui.drawGame(game.getBoard(), [0,0,0,0,0,0,0], optional=0)
        if game.getWinner():
                    break  
    if game.helper.isMoveValid(game.getBoard())==False:
        break
while True:
    gui.drawWinner(game.getWinner(), game.getBoard())
    
    



    #print game.getWinner()

    #while True:
        #move = gui.getPlayerMove(2, game.getBoard())
        #if game.dropPiece(move,2)==1:
            #break

