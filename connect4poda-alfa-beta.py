import random
import numpy as np
import pygame
import sys
import math

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

JOGADOR = 0
IA = 1

ESPACO_VAZIO = 0
PECA_JOGADOR = 1
PECA_IA = 2

def create_board():
	board = np.zeros((ROW_COUNT,COLUMN_COUNT))
	return board

def drop_piece(board, row, col, piece):
	board[row][col] = piece

def is_valid_location(board, col):
	return board[ROW_COUNT-1][col] == 0

def get_valid_locations(board):
	valid_locations = []
	for col in range(COLUMN_COUNT):
		if is_valid_location(board, col):
			valid_locations.append(col)
	return valid_locations

def get_next_open_row(board, col):
	for r in range(ROW_COUNT):
		if board[r][col] == 0:
			return r

def print_board(board):
	print(np.flip(board, 0))

def winning_move(board, piece):
	# Check horizontal locations for win
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT):
			if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
				return True

	# Check vertical locations for win
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
				return True

	# Check positively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(ROW_COUNT-3):
			if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
				return True

	# Check negatively sloped diaganols
	for c in range(COLUMN_COUNT-3):
		for r in range(3, ROW_COUNT):
			if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
				return True

def draw_board(board):
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):
			pygame.draw.rect(screen, BLUE, (c*SQUARESIZE, r*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
			pygame.draw.circle(screen, BLACK, (int(c*SQUARESIZE+SQUARESIZE/2), int(r*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
	
	for c in range(COLUMN_COUNT):
		for r in range(ROW_COUNT):		
			if board[r][c] == PECA_JOGADOR:
				pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
			elif board[r][c] == PECA_IA: 
				pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
	pygame.display.update()

def avaliar_posicao(board, piece):
	## avaliacao horizontal
	pontuacao = 0
	for r in range(ROW_COUNT):
		row_array = [int(i) for i in list(board[r,:])] # r,: significa que estamos pegando a linha r inteira junto com todas as colunas
		for c in range(COLUMN_COUNT-3):
			window = row_array[c:c+4]
			pontuacao += definir_valor_tela(window, piece)

	## avaliacao vertical
	for c in range(COLUMN_COUNT):
		col_array = [int(i) for i in list(board[:,c])]
		for r in range(ROW_COUNT-3):
			window = col_array[r:r+4]
			pontuacao += definir_valor_tela(window, piece)

	## avaliacao diagonal
	for r in range(ROW_COUNT-3):
		for c in range(COLUMN_COUNT-3):
			window = [board[r+i][c+i] for i in range(4)]
			pontuacao += definir_valor_tela(window, piece)
	return pontuacao

def definir_valor_tela(window, piece):
	pontuacao = 0
	peca_negativa = PECA_JOGADOR
	if piece == PECA_JOGADOR:
		peca_negativa = PECA_IA
	
	if window.count(piece) == 4: # pontuacao pra oportunidade de ganhar horizontalmente
		pontuacao += 100
	elif window.count(piece) == 3 and window.count(ESPACO_VAZIO) == 1: # pontuacao pra oportunidade de enfileirar 3 horizontalmente
		pontuacao += 10
	elif window.count(piece) == 2 and window.count(ESPACO_VAZIO) == 2:
		pontuacao += 4

	if window.count(peca_negativa) == 3 and window.count(ESPACO_VAZIO) == 1:
		pontuacao -= 8
	return pontuacao
'''
ROTINA minimax(nó, profundidade, maximizador)
    SE nó é um nó terminal OU profundidade = 0 ENTÃO
        RETORNE o valor da heurística do nó
    SENÃO SE maximizador é FALSE ENTÃO
        α ← +∞
        PARA CADA filho DE nó
            α ← min(α, minimax(filho, profundidade-1,true))
        FIM PARA
        RETORNE α
    SENÃO
        //Maximizador
        α ← -∞
        //Escolher a maior dentre as perdas causadas pelo minimizador
        PARA CADA filho DE nó
            α ← max(α, minimax(filho, profundidade-1,false))
        FIM PARA
        RETORNE α
    FIM SE
FIM ROTINA


function minimax(node, depth, maximizingPlayer) is
    if depth = 0 or node is a terminal node then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, minimax(child, depth − 1, FALSE))
        return value
    else (* minimizing player *)
        value := +∞
        for each child of node do
            value := min(value, minimax(child, depth − 1, TRUE))
        return value

'''
def minimax(board, depth, alfa, beta, maximizingPlayer):
	locais_validos = get_valid_locations(board)
	foi_lance_final = se_for_lance_final(board)
	if depth == 0 or foi_lance_final:
		if foi_lance_final:
			if winning_move(board, PECA_IA):
				return (100000000, None) # a ia ganhou
			elif winning_move(board, PECA_JOGADOR):
				return (-100000000, None) # o jogador ganhou
			else: 
				return (0, None) # situação de empate
		else:
			return avaliar_posicao(board, PECA_IA), None
	if maximizingPlayer:
		valor = -math.inf
		
		for col in locais_validos:
			row = get_next_open_row(board, col)
			copia_tabuleiro = board.copy()
			drop_piece(copia_tabuleiro, row, col, PECA_IA)
			novo_valor = minimax(copia_tabuleiro, depth-1, alfa, beta, False)[0]
			if novo_valor > valor:
				valor = novo_valor
				melhor_coluna = random.choice(locais_validos)
			alfa = max(alfa, valor)
			if alfa >= beta:
				break
		return valor, melhor_coluna
	else:
		valor = math.inf
		for col in locais_validos:
			row = get_next_open_row(board, col)
			copia_tabuleiro = board.copy()
			drop_piece(copia_tabuleiro, row, col, PECA_JOGADOR)
			novo_valor = minimax(copia_tabuleiro, depth-1, alfa, beta, True)[0]
			if novo_valor < valor:
				valor = novo_valor
				melhor_coluna = random.choice(locais_validos)
			beta = min(beta, valor)
			if alfa >= beta:
				break
		return valor, melhor_coluna	

def se_for_lance_final(board):
	return winning_move(board, PECA_JOGADOR) or winning_move(board, PECA_IA) or len(get_valid_locations(board)) == 0

def escolher_melhor_movimento(board, piece):
	valid_locations = get_valid_locations(board)
	melhor_pontuacao = 0
	melhor_coluna = random.choice(valid_locations)
	for col in valid_locations:	
		row = get_next_open_row(board, col)
		temp_board = board.copy()
		drop_piece(temp_board, row, col, piece)
		pontuacao = avaliar_posicao(temp_board, piece)
		print(pontuacao)
		# se a gente encontrar um caminho otimo, a gente escolhe esse caminho
		if pontuacao > melhor_pontuacao:
			melhor_pontuacao = pontuacao
			melhor_coluna = col
	return melhor_coluna


board = create_board()
print_board(board)
game_over = False


pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(JOGADOR, IA)

while not game_over:

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEMOTION:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			posx = event.pos[0]
			if turn == JOGADOR:
				pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)

		pygame.display.update()

		if event.type == pygame.MOUSEBUTTONDOWN:
			pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
			#print(event.pos)
			# Ask for Player 1 Input
			if turn == JOGADOR:
				posx = event.pos[0]
				col = int(math.floor(posx/SQUARESIZE))

				if is_valid_location(board, col):
					row = get_next_open_row(board, col)
					drop_piece(board, row, col, PECA_JOGADOR)

					if winning_move(board, PECA_JOGADOR):
						label = myfont.render("Player 1 wins!!", 1, RED)
						screen.blit(label, (40,10))
						game_over = True

					print_board(board)
					draw_board(board)

					turn += 1
					turn = turn % 2

	## Turno da IA		
	if turn == IA and not game_over:				
		
		valor_minimax, col  = minimax(board, 5, -math.inf, math.inf, True)

		if is_valid_location(board, col):
			pygame.time.wait(500)
			row = get_next_open_row(board, col)
			drop_piece(board, row, col, PECA_IA)

			if winning_move(board, PECA_IA):
				label = myfont.render("Player 2 wins!!", 1, YELLOW)
				screen.blit(label, (40,10))
				game_over = True

			print_board(board)
			draw_board(board)

			turn += 1
			turn = turn % 2

	if game_over:
		pygame.time.wait(3000)