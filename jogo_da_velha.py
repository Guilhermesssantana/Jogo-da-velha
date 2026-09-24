import pygame
import sys

# inicializar Pygame
pygame.init()

#constantes
WINDOW_SIZE = 300
GRID_SIZE = 100
LINE_WIDTH = 5

#cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (0, 0, 0)

# configuração da janela

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Jogo da Velha')

# logica do jogo
game_board =[[' ' for _ in range(3)] for _ in range (3)]
current_player = 'X'
def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all (board[row][col] == player for row in range(3)):
            return True
    if all (board[i][i] == player for i in range(3)) or all (board[i][2 - i] == player for i in range(3)):
        return True
return False

#desenho do jogo

