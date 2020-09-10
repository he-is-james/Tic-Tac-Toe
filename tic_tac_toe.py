import pygame
import sys
import time
from pygame.locals import *

XO = 'x'
winner = None
draw = None

#setting up the screen and game window
width = 400
height = 400
pygame.init()
screen = pygame.display.set_mode((width, height + 100), 0, 32)
pygame.display.set_caption("Tic-Tac-Toe")
board = [[None] * 3, [None] * 3, [None] * 3]

#colors/images
white = (255, 255, 255)
black = (0, 0, 0)
line = (255, 0, 0)
x_img = pygame.image.load("x_modified.png")
o_img = pygame.image.load("o_modified.png")
x_img = pygame.transform.scale(x_img, (80, 80))
o_img = pygame.transform.scale(o_img, (80, 80))


#initializing game by drawing the board
def opening_screen():
    time.sleep(3)
    screen.fill(white)
    pygame.draw.line(screen, black, (width/3, 0), (width/3, height), 7)
    pygame.draw.line(screen, black, (width/3*2, 0), (width/3*2, height), 7)
    pygame.draw.line(screen, black, (0, height/3), (width, height/3), 7)
    pygame.draw.line(screen, black, (0, height/3*2), (width, height/3*2), 7)
    status()

#check whether or not the game will continue or end in a draw
def status():
    global draw
    if winner is None:
        message = XO.upper() + " 's Turn"
    else:
        message = winner.upper() + " won!"
    if draw:
        message = "Game Draw!"
    font = pygame.font.Font(None, 30)
    text = font.render(message, 1, white)
    screen.fill(black, (0, 400, 500, 100))
    text_rect = text.get_rect(center=(width/2, 500-50))
    screen.blit(text, text_rect)
    pygame.display.update()


#determine how someone wins and who the winner is
def to_win():
    global board, winner, draw
    for row in range(0, 3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            winner = board[row][0]
            pygame.draw.line(screen, line, (0, (row+1)*height/3-height/6), (width, (row+1)*height/3-height/6), 4)
            break
    for col in range(0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            winner = board[0][col]
            pygame.draw.line(screen, line, ((col+1)*width/3-width/6, 0), ((col+1)*width/3-width/6, height), 4)
            break
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        winner = board[0][0]
        pygame.draw.line(screen, line, (50, 50), (350, 350), 4)
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        winner = board[0][2]
        pygame.draw.line(screen, line, (350, 50), (50, 350), 4)
    if all(all(row) for row in board) and winner is None:
        draw = True
    status()

    
#playing the game with two players
def placeXO(row, col):
    global board, XO
    if row == 1:
        posx = 30
    elif row == 2:
        posx = width / 3 + 30
    elif row == 3:
        posx = width / 3 * 2 + 30
    if col == 1:
        posy = 30
    elif col == 2:
        posy = height / 3 + 30
    elif col == 3:
        posy = height / 3 * 2 + 30
    board[row-1][col-1] = XO
    if XO == 'x':
        screen.blit(x_img, (posy, posx))
        XO = 'o'
    else:
        screen.blit(o_img, (posy, posx))
        XO = 'x'
    pygame.display.update()

#identifying where the player clicks to place their move
def click():
    x, y = pygame.mouse.get_pos()
    if x < width / 3:
        col = 1
    elif x < width / 3 * 2:
        col = 2
    elif x < width:
        col = 3
    else:
        col = None
    if y < height / 3:
        row = 1
    elif y < height / 3 * 2:
        row = 2
    elif y < height:
        row = 3
    else:
        row = None
    if row and col and board[row-1][col-1] is None:
        global XO
        placeXO(row, col)
        to_win()

        
#continue the game after the result
def reset():
    global board, winner, XO, draw
    time.sleep(3)
    XO = 'x'
    draw = False
    opening_screen()
    winner = None
    board = [[None]*3, [None]*3, [None]*3]

#starting the game on opening
def main():
    opening_screen()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type is MOUSEBUTTONDOWN:
                click()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reset()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        pygame.display.update()

        
while True:
    if __name__ == '__main__':
        main() 
