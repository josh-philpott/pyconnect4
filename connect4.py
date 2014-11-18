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

    def minimax(self, board, player, depth, maxDepth=100):
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
        #A potential move is guaranteed since isgameOver check has passed
        for i in range(0,7):
            potential_board = copy.deepcopy(board)
            if self.isMoveValid(potential_board,i):
                #print i, depth
                self.dropPiece(i,player,potential_board)
                scores.append(self.minimax(potential_board, opponent,depth+1, maxDepth)[1])
                moves.append(i)
                if max(scores)==scores[len(moves)-1]:
                    max_score_index = len(moves)-1
                if min(scores)==scores[len(moves)-1]:
                    min_score_index = len(moves)-1
            else:
                #if move is not valid, ensure it will not be selected
                if player==global_computer:
                    scores.append(-1000)
                else:
                    scores.append(1000)
        if depth==0:
            print scores
        
    
        if player == global_computer:
            #get moves that are "equivalent" to best move
            best_score = scores[max_score_index]
            best_moves = []
            for i in range(len(scores)):
                if scores[i]==best_score:
                    best_moves.append(i)
                    #target deeper play if bad outcome
                    if(best_score<0):
                        scores[i]=best_score + (maxDepth-depth)
            
            return random.choice(best_moves), scores[max_score_index]
        else:
            return moves[min_score_index], scores[min_score_index]
        
    #def getPotentialMoves(self, board, tile, lookAhead):
        #"""Get Potential Moves currently implemented on Baxter"""
                
        #if lookAhead == 0 or not self.isMoveValid(board):
            #return [0] * 7
    
        

        #if tile == 2:
            #enemyTile = 1
        #else:
            #enemyTile = 2

        ## Figure out the best move to make.
        #potentialMoves = [0] * 7
        #for firstMove in range(7):
            #dupeBoard = copy.deepcopy(board)
            #if not self.isMoveValid(dupeBoard, firstMove):
                #continue
            #self.dropPiece(firstMove, tile, dupeBoard)
            #if self.checkWinner(dupeBoard)==tile:
                ## a winning move automatically gets a perfect fitness
                #potentialMoves[firstMove] = 1
                #break  # don't bother calculating other moves
            #else:
                ## do other player's counter moves and determine best one
                #if not self.isMoveValid(dupeBoard):
                    #potentialMoves[firstMove] = 0
                #else:
                    #for counterMove in range(7):
                        #dupeBoard2 = copy.deepcopy(dupeBoard)
                        #if not self.isMoveValid(dupeBoard2, counterMove):
                            #continue
                        #self.dropPiece(counterMove, enemyTile, dupeBoard2)
                        #if self.checkWinner(dupeBoard)==enemyTile:
                            ## a losing move automatically gets the worst fit
                            #potentialMoves[firstMove] = -1
                            #break
                        #else:
                            ## do the recursive call to self.getPotentialMoves()
                            #results = self.getPotentialMoves(dupeBoard2, tile,
                                                             #lookAhead - 1)
                            #potentialMoves[firstMove] += (sum(results) / 7) / 7
        #return potentialMoves    

    def isMoveValid(self, board, col=None):
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
        """ Make move on current board. Returns 0 if move invalid """

        isMoveValid = self.helper.isMoveValid(self.board, col)

        if isMoveValid:
            self.helper.dropPiece(col, player, self.board)
            return 1
        else:
            return 0

    def getBoard(self):
        return self.board

    def getWinner(self):
        return self.helper.checkWinner(self.board)

    def makeComputerMove(self):
        move, score = self.helper.minimax(self.board, global_computer, 0, maxDepth=4)
        
        print "Moving to",move,"with a score of",score
        self.dropPiece(move, global_computer)
        #moves = self.helper.getPotentialMoves(self.board, self.computer, 4)
        #print moves

        ##first check for winning move
        #for i in range(0,7):
            #if moves[i]==1:
                #self.dropPiece(i, self.computer)
                #return

        #for i in range(0,7):
            #if moves[i]==0 and self.helper.isMoveValid(self.board, i):
                #self.dropPiece(i, self.computer)
                #return

        #for i in range(0,7):
            #if self.helper.isMoveValid(self.board, i):
                #self.dropPiece(i, self.computer)
                #return

        #return -1





        ##check if all moves are 0
        #all_zero = True
        #none_valid = True
        #valid = []
        #for i in range(0,7):
            #valid.append(self.helper.isMoveValid(self.board,i))
            #if valid[i]==1:
                #none_valid=False
            #if moves[i]!=0:
                #all_zero = False

        #if all_zero == True:
            ##pick random move, make sure it's valid, and drop piece
            #random.randint(0, 6)





class GUI:
    def __init__(self):
        pygame.init()

        #handle screen
        self.size = width, height = 900,800
        self.margin_top  = 100
        self.margin_left = 100
        self.screen = pygame.display.set_mode(self.size)

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

            self.clearScreen()
            self.drawTokens(player_move)
            self.drawBoard(board) 
            pygame.display.update()



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
        game.makeComputerMove()

    else:
        game.makeComputerMove()
        while True:
            move = gui.getPlayerMove(2, game.getBoard())
            if game.dropPiece(move,2)==1:
                break	



    #print game.getWinner()

    #while True:
        #move = gui.getPlayerMove(2, game.getBoard())
        #if game.dropPiece(move,2)==1:
            #break

