import pygame as pg
from random import randint, choice
from copy import deepcopy

# Размер окна

width = 500
height = 500

# Цвета линий и фона соответственно

line_color = (255, 255, 255)
bg_color = ((125, 192, 250))

board = [[0] * 3, [0] * 3, [0] * 3]

screen = pg.display.set_mode((width, height))  # Инициализация окна


# Выбор случайного движения из списка

def chooseRandomMoveFromList(board, movesList):
    possibleMoves = []
    for i in movesList:
        if board[i // 3][i % 3] == 0:
            possibleMoves.append(i)
    if len(possibleMoves) != 0:
        return choice(possibleMoves)
    else:
        return None


# Проверка состояния доски

def is_solved(board):
    boardT = list(map(list, zip(*board)))
    for elem, elem1 in zip(board, boardT):
        if elem == [1, 1, 1] or elem1 == [1, 1, 1] or [board[0][0], board[1][1], board[2][2]] == [1, 1, 1] or [
            board[0][2], board[1][1], board[2][0]] == [1, 1, 1]:
            return 1
        if elem == [2, 2, 2] or elem1 == [2, 2, 2] or [board[0][0], board[1][1], board[2][2]] == [2, 2, 2] or [
            board[0][2], board[1][1], board[2][0]] == [2, 2, 2]:
            return 2
    if 0 in board[0] + board[1] + board[2]:
        return -1
    return 0


# Заполнение фона

def make_bg():
    screen.fill(bg_color)
    pg.draw.line(screen, line_color, (width / 3, 0), (width / 3, height), 1)
    pg.draw.line(screen, line_color, (width / 3 * 2, 0), (width / 3 * 2, height), 1)
    pg.draw.line(screen, line_color, (0, height / 3), (width, height / 3), 1)
    pg.draw.line(screen, line_color, (0, height / 3 * 2), (width, height / 3 * 2), 1)


#  Начальная настройка окна

def setup():
    # Загрузка иконки
    Icon = pg.image.load('./ttt.png')
    pg.display.set_icon(Icon)
    # Название окна
    pg.display.set_caption('TicTacToes')
    # Загрузка изображений спрайтов
    x_img = pg.image.load("./x.png")
    o_img = pg.image.load("./o.png")
    # Трансформация спрайтов до необходимых размеров
    x_img = pg.transform.scale(x_img, (125, 125))
    o_img = pg.transform.scale(o_img, (125, 125))
    make_bg()
    pg.display.update()
    dice = roll_dice()
    return x_img, o_img, dice


#  Отрисовка доски

def render(board):
    for i in range(3):
        for j in range(3):
            if board[i][j] == 1:
                screen.blit(x_img, ((125 + 40) * j + 20, (125 + 40) * i + 20))
            elif board[i][j] == 2:
                screen.blit(o_img, ((125 + 40) * j + 20, (125 + 40) * i + 20))
            else:
                pg.draw.rect(screen, (125, 192, 250), ((125 + 40) * j + 20, (125 + 40) * i + 20, 125, 125))


# Очистка доски

def clear_board():
    global board
    board = [[0] * 3, [0] * 3, [0] * 3]
    make_bg()
    pg.display.update()


# Определение фигур для игроков в случайном порядке

def roll_dice():
    return randint(0, 1)


# Реализация хода компьютера

def AI():
    global board
    i, j = randint(0, 2), randint(0, 2)
    if not hard_AI:
        while board[i][j] != 0:
            i, j = randint(0, 2), randint(0, 2)
    else:
        i, j = real_AI(dice)
    board[i][j] = 2 if dice else 1
    render(board)
    pg.display.update()


# Реализация хода игрока 	

def on_click():
    global board
    x, y = pg.mouse.get_pos()

    if (x < width / 3):
        x = 0
    elif (x < width / 3 * 2):
        x = 1
    else:
        x = 2

    if (y < height / 3):
        y = 0
    elif (y < height / 3 * 2):
        y = 1
    else:
        y = 2
    if board[y][x] == 0:
        board[y][x] = 1 if dice else 2
    render(board)
    pg.display.update()


# Вывод сообщения о состоянии игры

def print_text(message):
    font = pg.font.Font(None, 50)
    text = font.render(message, 1, (255, 255, 255), (0, 0, 0))
    text_rect = text.get_rect(center=(width / 2, 250))
    screen.blit(text, text_rect)
    pg.display.update()


def real_AI(dice):
    global board

    # Проверяет возможность выигрыша своим ходом.

    for i in range(9):
        copy = deepcopy(board)
        if copy[i // 3][i % 3] == 0:
            copy[i // 3][i % 3] = 2 if dice else 1
            if dice:
                if is_solved(copy) == 2:
                    return i // 3, i % 3
            else:
                if is_solved(copy) == 1:
                    return i // 3, i % 3

    # Проверяет возможность выигрыша следующим ходом игрока, если да, то блокирует его.

    for i in range(9):
        copy = deepcopy(board)
        if copy[i // 3][i % 3] == 0:
            copy[i // 3][i % 3] = 1 if dice else 2
            if dice:
                if is_solved(copy) == 1:
                    return i // 3, i % 3
            else:
                if is_solved(copy) == 2:
                    return i // 3, i % 3

    # Пытается занимать углы если они свободны.

    move = chooseRandomMoveFromList(board, [0, 2, 6, 8])
    if move != None:
        return move // 3, move % 3

    # Пытается занять середину если она свободна.
    if board[1][1] == 0:
        return 1, 1
    move = chooseRandomMoveFromList(board, [1, 3, 5, 7])
    return move // 3, move % 3


pg.init()
x_img, o_img, dice = setup()
running = True
hard_AI = True  # флаг настоящего ИИ, в противном случае ходы компьютера будут случайными

while running:
    state = is_solved(board)
    if state == 1:
        print_text('You won!' if dice else 'You lost!')
        pg.display.update()
        pg.time.wait(1000)
        clear_board()
        dice = randint(0, 1)
    elif state == 2:
        print_text('You lost!' if dice else 'You won!')
        pg.display.update()
        pg.time.wait(1000)
        clear_board()
        dice = randint(0, 1)
    elif state == 0:
        print_text('Oh, it\'s a draw!')
        pg.display.update()
        pg.time.wait(1000)
        clear_board()
        dice = randint(0, 1)
    # получение событий из стека
    for event in pg.event.get():

        # проверка событий в стеке
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                on_click()
                state = is_solved(board)
                if state == -1:
                    pg.time.wait(1000)
                    AI()
