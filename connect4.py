#Last update - 12/1/14 @ 5:15PM

import pygame
import sys
import copy 
import random
import collections
#Dont modify these#####
global_computer = 2####
global_human = 1   ####
#######################

#Change these to use minimax/alpha beta
alphabeta_flag = True
search_depth = 6


class ConnectFourHelper:
    """ConnectFourHelper contains helper functions for ConnectFourGame """

    def __init__(self):
        pass

    def minimax(self,board,player,depth=0,maxDepth=8):   
        #if game is over or max depth is reached, return no move / score
        if self.isGameOver(board)==True or depth==maxDepth-1:
            sc=self.getScore(board,global_computer,depth)
            return 0, sc,1

        scores = []
        moves = []
        expanded_states = 1
        
        #For each possible move
        for i in range(0,7):
            #Evaluate if the move is valid
            if self.isMoveValid(board,i)==True:
                #simulate dropping piece on board
                potential_board = copy.deepcopy(board)
                if(player==1):
                    self.dropPiece(i,global_computer,potential_board)
                else:
                    self.dropPiece(i,global_human,potential_board) 
                #Run minimax on subgame. Increase depth by 1
                score,expanded = self.minimax(potential_board, (player%2)+1, depth+1, maxDepth)[1:]
                scores.append(score)
                moves.append(i)  
                #keep track of total expanded states
                expanded_states = expanded_states+expanded
                
        #Print scores for presentation purposes
        if depth==0:
            print scores
            
        #Maximize for player 1
        if player==1:
            max_score_indicies = [i for i, x in enumerate(scores) if x == max(scores)]
            max_score_index = random.choice(max_score_indicies)
            max_score = scores[max_score_index]
            move = moves[max_score_index]
            return move,max_score,expanded_states
        #Minimize for player 2
        else:
            min_score_indicies = [i for i, x in enumerate(scores) if x == min(scores)]
            min_score_index = random.choice(min_score_indicies)
            min_score = scores[min_score_index]
            move = moves[min_score_index]     
            return move, min_score,expanded_states
        
    def alphabeta(self,board,player,depth=0,maxDepth=8, alpha=-1000, beta=1000):      
        if self.isGameOver(board)==True or depth==maxDepth-1:
            sc=self.getScore(board,global_computer,depth)
            return -1, sc,1

        scores = []
        moves = []
        expanded_states = 1
        for i in range(0,7):
            if self.isMoveValid(board,i)==True:
                potential_board = copy.deepcopy(board)
                if(player==1):
                    self.dropPiece(i,global_computer,potential_board)
                elif(player==2):
                    self.dropPiece(i,global_human,potential_board)  
                else:
                    print "ERROR"
                score,expanded = self.alphabeta(potential_board, (player%2)+1, depth+1, maxDepth, alpha, beta)[1:]
                scores.append(score)
                expanded_states = expanded_states+expanded
                moves.append(i)
                if(player==1):
                    if(score>alpha):
                        alpha = score
                if(player==2):
                    if(score<beta):
                        beta = score
                if(alpha>=beta and depth!=0):
                    break                

        if depth==0:
            print scores

        if player==1:
            #return leftmost max score
            max_score_index = scores.index(max(scores))
            max_score = scores[max_score_index]
            move = moves[max_score_index]
            return move,max_score,expanded_states
        else:
            #return leftmost min score
            min_score_index = scores.index(min(scores))
            min_score = scores[min_score_index]
            move = moves[min_score_index]     
            return move, min_score,expanded_states



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

    def getScore(self, board, player,depth):
        """Return game score based off of win state"""
        if player==1:
            computer = 2
        else:
            computer = 1

        if self.checkWinner(board)==player:
            return 100-depth
        elif self.checkWinner(board)==computer:
            return depth-100
        else:
            threes = self.checkOpenThree(board)
            if(threes[0]>threes[1]):
                return depth-75
            elif(threes[1]>threes[0]):
                return 75-depth
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

    def checkOpenThree(self, board):
        """Check for the number of 3 in a rows"""
        threes = [0,0]

        #check horizontal
        for row in range (0,6):
            for start in range (0,4):
                if board[row][start]!=0:
                    #check for XXX_
                    if (board[row][start] == board[row][start+1] ==
                        board[row][start+2] and board[row][start+3] == 0):
                        threes[board[row][start]-1] = threes[board[row][start]-1] + 1

                    #check for _XXX
                    if (board[row][start] == 0 and board[row][start+1] ==
                        board[row][start+2] == board[row][start+3]):       
                        threes[board[row][start+1]-1] = threes[board[row][start+1]-1] + 1

                    #check for X_XX
                    if (board[row][start+1] == 0 and board[row][start] ==
                        board[row][start+2] == board[row][start+3]):   
                        threes[board[row][start]-1] = threes[board[row][start]-1] + 1

                    #check for XX_X   
                    if (board[row][start+2] == 0 and board[row][start] ==
                        board[row][start+1] == board[row][start+3]):   
                        threes[board[row][start]-1] = threes[board[row][start]-1] + 1  
            #Check for winner diagn - bottom-right to top-left
            for row in range (3,6):
                for start in range (0,4):
                    #check for _XXX
                    if (board[row][start] == 0 and board[row-1][start-1] ==
                        board[row-2][start-2] == board[row-3][start-3]):
                        threes[board[row-1][start-1]-1] = threes[board[row-1][start-1]-1] + 1
                    #check for X_XX
                    if (board[row-1][start-1] == 0 and board[row][start] ==
                        board[row-2][start-2] == board[row-3][start-3]):   
                        threes[board[row][start]-1] = threes[board[row][start]-1] + 1
                    #check for XX_X
                    if (board[row-2][start-2] == 0 and board[row][start] ==
                        board[row-1][start-1] == board[row-3][start-3]):   
                        threes[board[row][start]-1] = threes[board[row][start]-1] + 1  
                        #check for _XXX
                    if (board[row-3][start-3] == 0 and board[row-1][start-1] ==
                        board[row-2][start-2] == board[row][start]):
                        threes[board[row][start]-1] = threes[board[row][start]-1] + 1
            #Check for 3 diagn - bottom-left to top-right
            for row in range (0,3):
                for start in range (0,4):
                    #check for _XXX
                    if (board[row][start] == 0 and board[row+1][start+1] ==
                        board[row+2][start+2] == board[row+3][start+3]):
                        threes[board[row+1][start+1]-1] = threes[board[row+1][start+1]-1] + 1
                    #check for X_XX
                    if (board[row+1][start+1] == 0 and board[row][start] ==
                        board[row+2][start+2] == board[row+3][start+3]):   
                        threes[board[row][start]-1] = threes[board[row][start]-1] + 1
                    #check for XX_X
                    if (board[row+2][start+2] == 0 and board[row][start] ==
                        board[row+1][start+1] == board[row+3][start+3]):   
                        threes[board[row][start]-1] = threes[board[row][start]-1] + 1  
                        #check for _XXX
                    if (board[row+3][start+3] == 0 and board[row+1][start+1] ==
                        board[row+2][start+2] == board[row][start]):
                        threes[board[row][start]-1] = threes[board[row][start]-1] + 1
        return threes

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
        if alphabeta_flag==True:
            move, score, expanded_states = self.helper.alphabeta(self.board, 1, 0, maxDepth=search_depth)
        else:
            move, score, expanded_states = self.helper.minimax(self.board,1,0,maxDepth=search_depth)
        print "Moving to",move,"with a score of",score
        print "Expanded",expanded_states,"states"
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
