import pygame
import time
from pyautogui import alert


# dimensions
height = width = 800
block_size = 200
box_width = 600
pos = (width - box_width)/2

# colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)

# globals
data = 'x'
done = True
game_over = False
winner = ''
board = [
    ['', '', ''],
    ['', '', ''],
    ['', '', '']
]
player = 'player x'


# create window
window = pygame.display.set_mode((height, width))
pygame.display.set_caption("TIC TAC TOE")
pygame.init()

# fonts
font = pygame.font.Font('freesansbold.ttf', 40)
font1 = pygame.font.Font('freesansbold.ttf', 100)
font2 = pygame.font.Font('freesansbold.ttf', 60)
font3 = pygame.font.Font('freesansbold.ttf', 30)


# fill window with white color
def fill():
    window.fill(white)


# create grids for game
def grid():
    for x in range(0, box_width, block_size):
        for y in range(0, box_width, block_size):
            rect = pygame.Rect(x + pos, y + pos, block_size, block_size)
            pygame.draw.rect(window, black, rect, 1)

    for i in range(0, 3):
        for j in range(0, 3):
            text = font1.render(board[i][j], True, red)
            txt = text.get_rect(center=((block_size * (j + 1)) + (pos-(block_size/2)),
                                        (block_size * (i + 1)) + (pos-(block_size/2))))
            window.blit(text, txt)


# input values into array board
def set_data(block):
    q = int(block[0])
    p = int(block[1])
    if board[p][q] == '':
        board[p][q] = data
        return True


# change the current player
def player_change():
    global player, data
    if player == 'player x':
        player = 'player o'
        data = 'o'
        return player
    if player == 'player o':
        player = 'player x'
        data = 'x'
        return player


# display which player is playing now
def player_turn():
    text = font.render(f'{player}\'s turn', True, red)
    txt = text.get_rect()
    txt.center = (width/2, 50)
    window.blit(text, txt)


# check who is the winner
def check_winner():
    global done, game_over
    for i in range(0, 3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            x1, y1 = (pos+block_size/3), (pos+block_size/2) + (i * block_size)  # start and end point of line finding
            x2, y2 = (width-(pos+block_size/3)), (pos+block_size/2) + (i * block_size)
            draw_line(x1, y1, x2, y2)
            game_over = True
            return board[i][0]

        elif board[0][i] == board[1][i] == board[2][i] != '':
            x1, y1 = (pos+block_size/2) + (i * block_size), (pos+block_size/3)
            x2, y2 = (pos+block_size/2) + (i * block_size), width-(pos+block_size/3)
            draw_line(x1, y1, x2, y2)
            game_over = True
            return board[0][i]

        elif board[0][0] == board[1][1] == board[2][2] != '':
            x1, y1 = (pos+block_size/3), (pos+block_size/3)
            x2, y2 = width-(pos+block_size/3), width-(pos+block_size/3)
            draw_line(x1, y1, x2, y2)
            game_over = True
            return board[1][1]

        elif board[0][2] == board[1][1] == board[2][0] != '':
            x1, y1 = width-(pos+block_size/3), (pos+block_size/3)
            x2, y2 = (pos+block_size/3), width-(pos+block_size/3)
            draw_line(x1, y1, x2, y2)
            game_over = True
            return board[1][1]

        if '' not in board[0] and '' not in board[1] and '' not in board[2]:
            game_over = True
            return 'draw'


# draw line over the matching row
def draw_line(start_x, start_y, end_x, end_y):
    pygame.draw.line(window, black, (start_x, start_y), (end_x, end_y), width=4)


# fill text into the welcome window
def home_fill():
    window.fill(white)
    text = font2.render('TIC TAC TOE', True, red)
    txt = text.get_rect(center=(width/2, block_size))
    window.blit(text, txt)
    text = font3.render('_press space to start_', True, black)
    txt = text.get_rect(center=(width/2, height-block_size))
    window.blit(text, txt)


# create welcome window
def home():
    global done
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        home_fill()
        pygame.display.update()


# main game window
def main():
    global done, winner
    while done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = False

            if event.type == pygame.MOUSEBUTTONUP and not game_over:
                mouse_point = pygame.mouse.get_pos()
                mouse_point_change = map(lambda i, j: i - j, mouse_point, (pos, pos))
                grid_no = map(lambda i, j: i // j, tuple(mouse_point_change), (block_size, block_size))
                grid_no = tuple(grid_no)
                if 0 <= grid_no[0] < 3 and 0 <= grid_no[1] < 3:
                    if set_data(grid_no):
                        player_change()

        fill()
        grid()
        player_turn()
        winner = check_winner()
        pygame.display.update()
        if game_over:
            time.sleep(1)
            if winner == 'x' or winner == 'o':
                alert(f"player {winner} won", "winner")
                return
            elif winner == 'draw':
                alert(f"{winner} game", "winner")
                return


# clear the existing moves and reset global variables
def clear():
    global board, game_over, player, data, winner
    board = [
        ['', '', ''],
        ['', '', ''],
        ['', '', '']
    ]
    game_over = False
    player = 'player x'
    data = 'x'
    winner = ''


if __name__ == '__main__':
    while done:
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                done = False
        home()
        main()
        clear()
