import pygame
import sys

pygame.init()

# Configurações da janela
WINDOW_WIDTH = 420
WINDOW_HEIGHT = 520
PADDING = 30
BOARD_SIZE = 300
GRID_SIZE = BOARD_SIZE / 3

# Cores
BG = (9, 13, 24)
PANEL = (17, 24, 39)
BOARD = (18, 31, 52)
TEXT = (236, 248, 255)
MUTED = (148, 163, 184)
X_COLOR = (103, 232, 249)
O_COLOR = (244, 114, 182)
ACCENT = (96, 165, 250)
LINE_COLOR = (47, 72, 101)
WIN_COLOR = (52, 211, 153)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Jogo da Velha')

# Fonte
font_title = pygame.font.SysFont('arial', 26, bold=True)
font_status = pygame.font.SysFont('arial', 20, bold=True)
font_button = pygame.font.SysFont('arial', 18, bold=True)

# Lógica do jogo
game_board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'
game_over = False
winner = None


def reset_game():
    global game_board, current_player, game_over, winner
    game_board = [[' ' for _ in range(3)] for _ in range(3)]
    current_player = 'X'
    game_over = False
    winner = None


def check_win(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False


def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)


def draw_background():
    screen.fill(BG)

    # efeito de gradiente sutil
    for y in range(0, WINDOW_HEIGHT, 6):
        alpha = min(255, y * 0.6)
        color = (int(9 + alpha * 0.03), int(13 + alpha * 0.04), int(24 + alpha * 0.07))
        pygame.draw.line(screen, color, (0, y), (WINDOW_WIDTH, y), 6)

    panel_rect = pygame.Rect(18, 18, WINDOW_WIDTH - 36, WINDOW_HEIGHT - 36)
    pygame.draw.rect(screen, PANEL, panel_rect, border_radius=26)

    pygame.draw.rect(screen, (18, 31, 52), (42, 82, 336, 336), border_radius=18)


def draw_status():
    if game_over:
        if winner:
            text = f'Jogador {winner} venceu!'
            color = WIN_COLOR
        else:
            text = 'Empate!'
            color = MUTED
    else:
        text = f'Vez do jogador {current_player}'
        color = X_COLOR if current_player == 'X' else O_COLOR

    label = font_status.render(text, True, color)
    screen.blit(label, (WINDOW_WIDTH // 2 - label.get_width() // 2, 52))


def draw_board_grid():
    board_x = 60
    board_y = 100
    offset = BOARD_SIZE / 3

    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (board_x + i * offset, board_y),
                         (board_x + i * offset, board_y + BOARD_SIZE), 4)
        pygame.draw.line(screen, LINE_COLOR, (board_x, board_y + i * offset),
                         (board_x + BOARD_SIZE, board_y + i * offset), 4)


def draw_x(row, col):
    board_x = 60
    board_y = 100
    cell = BOARD_SIZE / 3
    offset = 26
    x1 = board_x + col * cell + offset
    y1 = board_y + row * cell + offset
    x2 = board_x + (col + 1) * cell - offset
    y2 = board_y + (row + 1) * cell - offset
    x3 = board_x + (col + 1) * cell - offset
    y3 = board_y + row * cell + offset
    x4 = board_x + col * cell + offset
    y4 = board_y + (row + 1) * cell - offset

    for i in range(10, 0, -1):
        pygame.draw.line(screen, (18, 131, 146, 100), (x1, y1), (x2, y2), 10 - i)
        pygame.draw.line(screen, (18, 131, 146, 100), (x3, y3), (x4, y4), 10 - i)

    pygame.draw.line(screen, X_COLOR, (x1, y1), (x2, y2), 6)
    pygame.draw.line(screen, X_COLOR, (x3, y3), (x4, y4), 6)


def draw_o(row, col):
    board_x = 60
    board_y = 100
    cell = BOARD_SIZE / 3
    center_x = board_x + col * cell + cell / 2
    center_y = board_y + row * cell + cell / 2
    radius = 34

    for i in range(10, 0, -1):
        pygame.draw.circle(screen, (168, 85, 247), (int(center_x), int(center_y)), radius + i, 4)

    pygame.draw.circle(screen, O_COLOR, (int(center_x), int(center_y)), radius, 6)


def draw_button():
    button_rect = pygame.Rect(110, 450, 200, 42)
    color = (96, 165, 250) if not game_over else (52, 211, 153)
    hover = False
    if hover:
        color = (125, 211, 252)

    pygame.draw.rect(screen, color, button_rect, border_radius=14)
    label = font_button.render('NOVO JOGO', True, (15, 23, 42))
    screen.blit(label, (button_rect.centerx - label.get_width() // 2, button_rect.centery - label.get_height() // 2 + 1))


def draw_board_symbols():
    for row in range(3):
        for col in range(3):
            if game_board[row][col] == 'X':
                draw_x(row, col)
            elif game_board[row][col] == 'O':
                draw_o(row, col)


running = True
while running:
    draw_background()
    draw_status()
    draw_board_grid()
    draw_board_symbols()
    draw_button()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            if 110 <= x <= 310 and 450 <= y <= 492:
                reset_game()
                continue

            if not game_over:
                board_x = 60
                board_y = 100
                cell_size = BOARD_SIZE / 3
                row = int((y - board_y) // cell_size)
                col = int((x - board_x) // cell_size)

                if 0 <= row < 3 and 0 <= col < 3 and game_board[row][col] == ' ':
                    game_board[row][col] = current_player

                    if check_win(game_board, current_player):
                        winner = current_player
                        game_over = True
                    elif is_board_full(game_board):
                        winner = None
                        game_over = True
                    else:
                        current_player = 'O' if current_player == 'X' else 'X'

    pygame.display.flip()

pygame.quit()
sys.exit()

