import numpy as np
import pygame
import sys
import math
import random

#x_in_a_row = int(input('Hvor mange på rad?: '))
x_in_a_row = 4  # Begrenser det til 4 på rad for øyeblikket
Row_count = int(input('Hvor mange rader vil du ha? (vertikalt): '))
Coloumn_count = int(input('Hvor mange kolonner vil du ha? (horisontalt): '))
player_name = input('Spillernavn : ')
player_1 = 0
AI = 1
Even = 0
Odd = 1
Blue = (0,0,255) # rgb verdier, dette gir veldig blå farge
Black = (0,0,0)
Red = (255,0,0)
Yellow = (255,255,0)
White = (255,255,255)
Empty = 0
Player_piece = 1
AI_piece = 2
turn = int(input('Hvem begynner? (1 eller 2): '))-1

def create_board():
    board = np.zeros((Row_count, Coloumn_count))
    return board

def valid(board, position):
    for i in range(Row_count):
        if board[i][position] == 0:
            return True
    return False

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[Row_count - 1][col] == 0

def get_next_open_row(board, col):
    for i in range(Row_count):
        if board[i][col] == 0:
            return i

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Horizontal
    for i in range(Coloumn_count - (x_in_a_row - 1)):  # minus 3 siden det trengs 4 på rad, mindre å sjekke
        for j in range(Row_count):
            if board[j][i] == piece and board[j][i+1] == piece and board[j][i+2] == piece and board[j][i+3] == piece:
                return True
    # Vertical
    for i in range(Coloumn_count):  # minus 3 siden det trengs 4 på rad, mindre å sjekke
        for j in range(Row_count - (x_in_a_row - 1)):
            if board[j][i] == piece and board[j+1][i] == piece and board[j+2][i] == piece and board[j+3][i] == piece:
                return True

    # Diagonally positively sloped
    for i in range(Coloumn_count - (x_in_a_row - 1)):  # minus 3 siden det trengs 4 på rad, mindre å sjekke
        for j in range(Row_count - (x_in_a_row - 1)):
            if board[j][i] == piece and board[j+1][i+1] == piece and board[j+2][i+2] == piece and board[j+3][i+3] == piece:
                return True

    # Diagonally negatively sloped
    for i in range(Coloumn_count - (x_in_a_row - 1)):  # minus 3 siden det trengs 4 på rad, mindre å sjekke
        for j in range((x_in_a_row - 1), Row_count):
            if board[j][i] == piece and board[j-1][i+1] == piece and board[j-2][i+2] == piece and board[j-3][i+3] == piece:
                return True

def evaluate_window(window, piece):
    score = 0
    opponent_piece = Player_piece
    if piece == Player_piece:
        opponent_piece = AI_piece

    if window.count(piece) == x_in_a_row:
        score += 100
    elif window.count(piece) == (x_in_a_row - 1) and window.count(Empty) == 1:
        score += 5
    elif window.count(piece) == (x_in_a_row - 2) and window.count(Empty) == 2:
        score += 2

    if window.count(opponent_piece) == (x_in_a_row - 1) and window.count(Empty) == 1:
        score -= 4
    return score


def score_position(board, piece):
    score = 0
    #Score center coloumn
    center_array = [int(i) for i in list(board[:, Coloumn_count//2])]
    center_count = center_array.count(piece)
    score += center_count*3


    # Horizontal
    for r in range(Row_count):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(Coloumn_count-(x_in_a_row - 1)):
            window = row_array[c:c+x_in_a_row]
            score += evaluate_window(window, piece)

    # Vertical
    for c in range(Coloumn_count):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(Row_count-(x_in_a_row-1)):
            window = col_array[r:r+x_in_a_row]
            score += evaluate_window(window, piece)

    # Positive sloped diagonal
    for r in range(Row_count-(x_in_a_row-1)):
        for c in range(Coloumn_count - (x_in_a_row - 1)):
            window = [board[r+i][c+i] for i in range(x_in_a_row)]
            score += evaluate_window(window, piece)

    # Negatively sloped diagonal
    for r in range(Row_count-(x_in_a_row-1)):
        for c in range(Coloumn_count - (x_in_a_row - 1)):
            window = [board[r+(x_in_a_row-1)-i][c+i] for i in range(x_in_a_row)]
            score += evaluate_window(window, piece)
    return score

def is_terminal_node(board):
    return winning_move(board, Player_piece) or winning_move(board, AI_piece) or len(get_valid_locations(board)) == 0

def minimax(board, depth, maximizingPlayer): # Hentet fra wikipedia pseudokode
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_piece):
                return (None, 100000) # stort tall bare
            elif winning_move(board, Player_piece):
                return (None, -1000000) # lavt tall bare
            else: # game over
                return (None, 0)
        else: #depth er null
            return  (None, score_position(board, AI_piece))
    if maximizingPlayer:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_piece)
            new_score = minimax(b_copy, depth-1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value
    else: #minimizingPlayer
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, Player_piece)
            new_score = minimax(b_copy, depth-1, True)[1]
            if new_score < value:
                value = new_score
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(Coloumn_count):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -1000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy() # lager en kopi av brettet som gjør det mulig å beregne score for neste trekk
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col
    return best_col

def draw_board(board):
    for i in range(Coloumn_count):
        for j in range(Row_count):
            pygame.draw.rect(screen, Blue, (i*squaresize, j*squaresize+squaresize, squaresize, squaresize))
            pygame.draw.circle(screen, Black, (int(i*squaresize+squaresize/2), int(j*squaresize+squaresize+squaresize/2)), radius)
    for i in range(Coloumn_count):
        for j in range(Row_count):
            if board[j][i] == Player_piece:
                pygame.draw.circle(screen, Red, (int(i*squaresize+squaresize/2), height-int(j*squaresize+squaresize/2)), radius)
            elif board[j][i] == AI_piece:
                pygame.draw.circle(screen, Yellow, (int(i*squaresize+squaresize/2), height-int(j*squaresize+squaresize/2)), radius)
    pygame.display.update()


game_over = False
board = create_board()
pygame.init()
squaresize = 100
width = Coloumn_count * squaresize
height = (Row_count+1) * squaresize
size = (width, height)
radius = int(squaresize/2 - 5)
screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont('monospace', 75)


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, Black, (0,0, width, squaresize))
            posx = event.pos[0]
            if turn == player_1:
                pygame.draw.circle(screen, Red, (posx, int(squaresize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, Black, (0, 0, width, squaresize))
            if turn == player_1:
                posx = event.pos[0] # event.pos gir en x og y verdi mellom 0 og 700 (pga width og height) der du trykker
                col = int(math.floor(posx/squaresize)) # runder ned og gir et tall mellom 0 og 6 (radene)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, Player_piece)

                    if winning_move(board, Player_piece):
                        label = myfont.render(f'{player_name} vant!!', 1, White)
                        screen.blit(label, (40,10))
                        game_over = True

                    turn = (turn+1)%2
                    draw_board(board)

    if turn == AI and not game_over:
        # col = random.randint(0, Coloumn_count-1) # dersom man ønsker helt tilfeldig trekk av AI
        # col = pick_best_move(board, AI_piece) # En mulighet, men minimax er en mye bedre AI
        col, minimax_score = minimax(board, 4, True) # Endre på tallet her for å endre hvor mange trekk AI tenker frem i tid
        if is_valid_location(board, col):
            pygame.time.wait(500)
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_piece)

            if winning_move(board, AI_piece):
                label = myfont.render('AI vant!!', 2, White)
                screen.blit(label, (40, 10))
                game_over = True

            turn = (turn + 1) % 2
            print_board(board)
            draw_board(board)

        if game_over:
             pygame.time.wait(5000)


