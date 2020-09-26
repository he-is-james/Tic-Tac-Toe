import pygame
import sys
import time
from pygame.locals import *

XO = 'x'
winner = None
draw = None

single_player = None
player = 'x'
computer = 'o'

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
end = (0, 150, 150)
x_img = pygame.image.load("x_modified.png")
o_img = pygame.image.load("o_modified.png")
x_img = pygame.transform.scale(x_img, (80, 80))
o_img = pygame.transform.scale(o_img, (80, 80))


#initializing game by drawing the board
def draw_board():
    time.sleep(3)
    screen.fill(white)
    pygame.draw.line(screen, black, (width/3, 0), (width/3, height), 7)
    pygame.draw.line(screen, black, (width/3*2, 0), (width/3*2, height), 7)
    pygame.draw.line(screen, black, (0, height/3), (width, height/3), 7)
    pygame.draw.line(screen, black, (0, height/3*2), (width, height/3*2), 7)
    status()

#two buttons that decide the mode
def mode():
    global draw
    font = pygame.font.Font(None, 25)
    text1 = font.render("Single Player (S)", 1, white, line)
    text2 = font.render("Two Players (T)", 1, white, line)
    text_rect1 = text1.get_rect(center=(width/6, 500-50))
    text_rect2 = text2.get_rect(center=(width/6*5, 500-50))
    screen.blit(text1, text_rect1)
    screen.blit(text2, text_rect2)
    pygame.display.update()

#endscreen for after a round is over
def endscreen():
    font = pygame.font.Font(None, 50)
    text = font.render("Game Over", 1, white)
    font1 = pygame.font.Font(None, 30)
    text1 = font1.render("Press 'r' to restart or 'q' to quit", 1, white)
    pygame.draw.rect(screen, end, (45, 150, 315, 150))
    text_rect = text.get_rect(center=(width/2, 200))
    text1_rect = text1.get_rect(center=(width/2, 250))
    screen.blit(text, text_rect)
    screen.blit(text1, text1_rect)
    pygame.display.update()


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


#Minimax Algorithm for the AI to make moves based on the player's choice
#checks if the game is still playable
def space_left():
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                return True
    return False

#determines the value of a player's move to minimize the potential loss
def evaluate():
    global board, winner, draw
    for row in range(0, 3):
        if (board[row][0] == board[row][1] == board[row][2]) and (board[row][0] is not None):
            if board[row][0] == player:
                return 10
            elif board[row][0] == computer:
                return -10
    for col in range(0, 3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            if board[0][col] == player:
                return 10
            elif board[0][col] == computer:
                return -10
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        if board[0][0] == player:
            return 10
        elif board[0][0] == computer:
            return -10
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        if board[0][2] == player:
            return 10
        if board[0][2] == computer:
            return -10
    if not space_left():
        return 0
    return -1

def minimax(m, d, a, b):
    score = evaluate()
    if score != -1:
        return score
    if m:
        best = -1000000
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = player
                    value = minimax(not m, d+1, a, b)
                    board[i][j] = None
                    best = max(best, value)
                    a = max(best, a)
                    if b <= a:
                        return a - d
        return a - d
    else:
        best = 1000000
        for i in range(3):
            for j in range(3):
                if board[i][j] is None:
                    board[i][j] = computer
                    value = minimax(not m, d+1, a, b)
                    board[i][j] = None
                    best = min(best, value)
                    b = min(best, b)
                    if b <= a:
                        return b + d
        return b + d

#decides where the AI will place its move
def next_move():
    now = 1000000
    move = [-1, -1]
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = computer
                move_value = minimax(True, 1, -1000000, 1000000)
                board[i][j] = None
                if move_value < now:
                    now = move_value
                    move = [i+1, j+1]
    return move

def ai_move():
    row, column = next_move()
    placeXO(row, column)

        
#continue the game after the result
def reset():
    global board, winner, XO, draw
    time.sleep(2)
    XO = 'x'
    single_player = None
    draw = False
    draw_board()
    mode()
    winner = None
    board = [[None]*3, [None]*3, [None]*3]

#starting the game on opening
def main():
    global single_player, XO
    draw_board()
    mode()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    single_player = True
                elif event.key ==pygame.K_t:
                    single_player = False
                if event.key == pygame.K_r:
                    reset()
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            if single_player is False:
                if event.type is MOUSEBUTTONDOWN:
                        click()
                if winner is not None:
                    endscreen()
            if single_player is True:
                if XO == 'x':
                    if event.type is MOUSEBUTTONDOWN:
                        click()
                else:
                    if draw is True:
                        break
                    ai_move()
                    to_win()
                    status()
                if winner is not None or draw is True:
                    endscreen()
        pygame.display.update()

        
while True:
    if __name__ == '__main__':
        main()
