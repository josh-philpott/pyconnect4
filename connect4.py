import pygame
import sys
import copy 

class ConnectFourHelper:
    """ConnectFourHelper contains helper functions for ConnectFourGame """

    def __init__(self):
	pass

    def alphaBeta(self, player, depth, board, alpha, beta):
	#score= -1
	#best = -1
	
	#boards = self.getPossibleBoards(player)
	
	#Check for winner
	if self.checkWinner==player:
	    return sys.maxint-depth
	elif self.checkWinner!=None:
	    return -(sys.maxint - depth)
	elif self.isMovePossible(board)==False:
	    return 0
	elif (depth==0):
	    #return current state heuristic
	    pass
	else:
	    best = -sys.maxint
	    max_alpha = alpha
	    #for each possible drop
	    for i in range(0,7):
		self.isMovePossible(board, i)		
		    
    def isMovePossible(self, board, col=None):
	if col==None:
	    for i in range(0,7):
		if board[0][i]==0:
		    return True
	    return False
	else:
	    if board[0][col]==0:
		return True
	    return False    
	    
	    

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
	    """ Make move on current board. Returns -1 if move invalid """
	
	    for i in range(5,-1,-1):
		if board[i][col]==0:
		    board[i][col]=player
		    return board
	    return None  
    

    
class ConnectFourGame:
    
    helper = ConnectFourHelper()
    
    def __init__(self):
	self.board = [[0,0,0,0,0,0,0],
	            [0,0,0,0,0,0,0],
	            [0,0,0,0,0,0,0],
	            [0,0,0,0,0,0,0],
	            [0,0,0,0,0,0,0],
	            [0,0,0,0,0,0,0]]    
	
    def dropPiece(self, col, player):
	""" Make move on current board. Returns 0 if move invalid """
	
	isMovePossible = self.helper.isMovePossible(self.board, col)
	
	if isMovePossible:
	    self.board = self.helper.dropPiece(col, player, self.board)
	    return 1
	else:
	    return 0
	
    def getBoard(self):
	return self.board
    
    def getWinner(self):
	return self.helper.checkWinner(self.board)


    

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

gui = GUI()
game = ConnectFourGame()

while True:  
    while True:
	move = gui.getPlayerMove(1, game.getBoard())
	if game.dropPiece(move,1)==1:
	    break
	  
    print game.getWinner()
        
    while True:
	move = gui.getPlayerMove(2, game.getBoard())
	if game.dropPiece(move,2)==1:
	    break
	
    print game.getWinner()