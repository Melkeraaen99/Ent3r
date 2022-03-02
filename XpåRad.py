import numpy as np
import pygame
import sys
import math

'''
def start():
    x_in_a_row = int(input('Hvor mange på rad?: '))
    if x_in_a_row < 3:
        x_in_a_row = int(input('Minste mulig er 3, hvor mange på rad?: '))
    Row_count = int(input('Hvor mange rader vil du ha? (vertikalt): '))
    if Row_count < x_in_a_row:
        Row_count = int(input('Du må ha flere rader enn det, hvor mange rader vil du ha?: '))
    Coloumn_count = int(input('Hvor mange kolonner vil du ha? (horisontalt): '))
    if Coloumn_count < x_in_a_row:
        Coloumn_count = int(input('Du må ha flere kolonner enn det, hvor mange kolonner vil du ha?: '))
    return x_in_a_row, Row_count, Coloumn_count

start = start()
'''

x_in_a_row = int(input('Hvor mange på rad?: '))
Row_count = int(input('Hvor mange rader vil du ha? (vertikalt): '))
Coloumn_count = int(input('Hvor mange kolonner vil du ha? (horisontalt): '))
player_1 = input('Spillernavn 1: ')
player_2 = input('Spillernavn 2: ')
turn = int(input('Hvem begynner? (1 eller 2): '))-1
Even = 0
Odd = 1
Blue = (0,0,255) # rgb verdier, dette gir veldig blå farge
Black = (0,0,0)
Red = (255,0,0)
Yellow = (255,255,0)
White = (255,255,255)

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

def draw_board(board):
    for i in range(Coloumn_count):
        for j in range(Row_count):
            pygame.draw.rect(screen, Blue, (i*squaresize, j*squaresize+squaresize, squaresize, squaresize))
            pygame.draw.circle(screen, Black, (int(i*squaresize+squaresize/2), int(j*squaresize+squaresize+squaresize/2)), radius)
    for i in range(Coloumn_count):
        for j in range(Row_count):
            if board[j][i] == 1:
                pygame.draw.circle(screen, Red, (int(i*squaresize+squaresize/2), height-int(j*squaresize+squaresize/2)), radius)
            elif board[j][i] == 2:
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
            if turn == 0:
                pygame.draw.circle(screen, Red, (posx, int(squaresize/2)), radius)
            else:
                pygame.draw.circle(screen, Yellow, (posx, int(squaresize/2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, Black, (0, 0, width, squaresize))
            if turn == 0:
                posx = event.pos[0] # event.pos gir en x og y verdi mellom 0 og 700 (pga width og height) der du trykker
                col = int(math.floor(posx/squaresize)) # runder ned og gir et tall mellom 0 og 6 (radene)
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render(f'{player_1} vant!!', 1, White)
                        screen.blit(label, (40,10))
                        game_over = True

            else:
                posx = event.pos[0]
                col = int(math.floor(posx / squaresize))
                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render(f'{player_2} vant!!', 1, White)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn = (turn+1)%2

            if game_over:
                pygame.time.wait(5000)
