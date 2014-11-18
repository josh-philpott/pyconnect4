import pygame
import sys
import copy 

class ConnectFour:
    """ConnectFour class handles all game logic"""

    def __init__(self):
	self.board = [[0,0,0,0,0,0,0],
	              [0,0,0,0,0,0,0],
	              [0,0,0,0,0,0,0],
	              [0,0,0,0,0,0,0],
	              [0,0,0,0,0,0,0],
	              [0,0,0,0,0,0,0]]

    def checkWinner(self):
	"""Returns winner. Check for all possible winning combinations"""

	#Check for winner horizontal
	for row in range (0,6):
	    for start in range (0,4):
		if self.board[row][start]!=0:
		    if (self.board[row][start] == self.board[row][start+1] ==
		        self.board[row][start+2] == self.board[row][start+3]):
			return self.board[row][start]

	#Check for winner diagn - bottom-left to top-right
	for row in range (0,3):
	    for start in range (0,4):
		if self.board[row][start]!=0:
		    if (self.board[row][start] == self.board[row+1][start+1] ==
		        self.board[row+2][start+2] == self.board[row+3][start+3]):
			return self.board[row][start]

	#Check for winner diagn - top-left to bottom-right
	for row in range (3,6):
	    for start in range (0,4):
		if self.board[row][start]!=0:
		    if (self.board[row][start] == self.board[row-1][start+1] ==
		        self.board[row-2][start+2] == self.board[row-3][start+3]):
			return self.board[row][start]

	#Check for winner vertical
	for row in range (0,3):
	    for start in range (0,7):
		if self.board[row][start]!=0:
		    if (self.board[row][start] == self.board[row+1][start] ==
		        self.board[row+2][start] == self.board[row+3][start]):
			return self.board[row][start]		


    def getBoard(self):
	"""Returns curent board state"""
	return self.board

    def getPossibleBoards(self, player):
	"""Returns list of possible boards"""
	board_states = []

	for col in range(0,7):
	    for row in range(5,-1,-1):
		temp_board = []
		if self.board[row][col]==0:
		    temp_board = copy.deepcopy(self.board)
		    temp_board[row][col]=player
		    board_states.append(temp_board)
		    break
	return board_states

    def makeMove(self, move, player):
	""" Make move on current board. Returns -1 if move invalid """

	for i in range(5,-1,-1):
	    if self.board[i][move]==0:
		self.board[i][move]=player
		return 0
	return -1

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
game = ConnectFour()

while True:  
    move = gui.getPlayerMove(1, game.getBoard())
    game.makeMove(move, 1)
    print game.checkWinner()
    move = gui.getPlayerMove(2, game.getBoard())
    game.makeMove(move, 2)
    print game.checkWinner()
