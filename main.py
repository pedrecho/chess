import copy
import datetime


_A = 65
_a = 97
_0 = 48


def message(number):
    if number == 0:
        return 'Некорректный ввод'
    if number == 1:
        return 'Некорректный ход: нет фигуры в заданной клетке'
    if number == 2:
        return 'Некорректный ход: выбранная фигура не может так ходить'
    if number == 3:
        return 'Некорректный ход: нельзя атаковать собственные фигуры'
    if number == 4:
        return 'Некорректный ход: сейчас ходят фигуры другого цвета'
    if number == 5:
        return 'Ничья: трёхкратное повторение позиции'
    if number == 6:
        return 'Ничья: пат'


def convert_to_alpha(digit):
    return chr(digit + _a)


def convert_from_alpha(symbol):
    return ord(symbol.lower()) - _a


def convert_to_number(digit):
    return chr(8 - digit + _0)


def convert_from_number(symbol):
    return 8 - ord(symbol.lower()) + _0


def show_board(board):
    print('   A B C D E F G H\n')
    for i in range(8):
        print(8 - i, end='  ')
        for ii in board[i]:
            print(ii, end=' ')
        print(' ', 8 - i)
    print('\n   A B C D E F G H')


def create_board():
    return [['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.', '.'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']]


def pawn(y, x, move, board, color):
    a, b, c = ([1, 2, 1], [-1, -2, 6])[color]
    if x != 0:
        return (False, True)[x == 1 and move[1][0] - move[0][0] == a and board[move[1][0]][move[1][1]] != '.']
    if move[1][0] - move[0][0] == a and board[move[1][0]][move[1][1]] == '.':
        return True
    if move[1][0] - move[0][0] == b and move[0][0] == c and board[move[1][0]][move[1][1]] == '.' and \
            board[(move[1][0] + move[0][0]) // 2][move[0][1]] == '.':
        return True
    return False


def knight(y, x):
    return (False, True)[x == 1 and y == 2 or x == 2 and y == 1]


def bishop(y, x, move, board):
    if x == y:
        ry = (move[1][0] - move[0][0]) // y
        rx = (move[1][1] - move[0][1]) // x
        for i in range(1, x):
            if board[move[0][0] + ry * i][move[0][1] + rx * i] != '.':
                return False
        return True
    return False


def rook(y, x, move, board):
    if x == 0 or y == 0:
        ry = (move[1][0] - move[0][0]) // max(1, y)
        rx = (move[1][1] - move[0][1]) // max(1, x)
        for i in range(1, max(x, y)):
            if board[move[0][0] + ry * i][move[0][1] + rx * i] != '.':
                return False
        return True
    return False


def queen(y, x, move, board):
    return bishop(y, x, move, board) or rook(y, x, move, board)


def king(y, x):
    return (False, True)[x <= 1 and y <= 1]


def possible_moves(board, move):
    figure = board[move[0][0]][move[0][1]].lower()
    y = abs(move[0][0] - move[1][0])
    x = abs(move[0][1] - move[1][1])
    # print(figure, y, x)
    if x + y == 0:
        return False
    if figure == 'p':
        return pawn(y, x, move, board, ord(board[move[0][0]][move[0][1]]) < _a)
    if figure == 'n':
        return knight(y, x)
    if figure == 'b':
        return bishop(y, x, move, board)
    if figure == 'r':
        return rook(y, x, move, board)
    if figure == 'q':
        return queen(y, x, move, board)
    if figure == 'k':
        return king(y, x)


def potential_moves(y, x, board):
    for i in range(8):
        for l in range(8):
            move = [[y, x], [i, l]]
            if possible_moves(board, move) and not same_colors(move, board):
                # print(i, l, board[y][x], board[i][l])
                return True
    return False


def potential_cell(y, x, color, board):
    for i in range(8):
        for l in range(8):
            if (ord(board[i][l]) < _a) == color:
                if possible_moves(board, [[i, l], [y, x]]):
                    return (i, l)
    return False


def same_colors(move, board):
    return (board[move[1][0]][move[1][1]] != '.') and (
            (ord(board[move[0][0]][move[0][1]]) < _a) == (ord(board[move[1][0]][move[1][1]]) < _a))


def figure_is_here(figure, color, board):
    cells = []
    for i in range(8):
        for l in range(8):
            if board[i][l] == (figure.lower(), figure.upper())[color]:
                cells.append([i, l])
    return cells


def pat(color, board):
    for i in range(8):
        for l in range(8):
            if (ord(board[i][l]) < _a) == color:
                if potential_moves(i, l, board):
                    return False
    return not (True, False)[potential_cell(figure_is_here('k', color, board), not color, board) == False]


def journal(move, board):
    rtn = ""
    figure = board[move[0][0]][move[0][1]]
    if figure.upper() != "P":
        rtn += figure.upper()
    figures = figure_is_here(figure, (False, True)[ord(figure) < _a], board)
    for i in figures:
        if possible_moves(board, [[i[0], i[1]], [move[1][0], move[1][1]]]):
            print(i[0], i[1])
            print(convert_to_alpha(i[1]), convert_to_number(i[0]))
            if i[0] == move[0][0] and i[1] != move[0][1]  and board[i[0]][i[1]].lower() != 'p':
                rtn += convert_to_alpha(move[0][1])
                break
            if i[1] == move[0][1] and i[0] != move[0][0]:
                rtn += convert_to_number(move[0][0])
                break
    if board[move[1][0]][move[1][1]] != '.':
        if board[move[0][0]][move[0][1]].lower() == 'p':
            rtn += convert_to_alpha(move[0][1])
        rtn += 'x'
    rtn += convert_to_alpha(move[1][1]) + convert_to_number(move[1][0]) + ' '
    return rtn


def write_match(moves):
    answers = ['[Event "' + input('Введите название турнира:') + '"]',
               '[Site "' + input('Введите местоположение:') + '"]', '[Date "' + str(datetime.date.today()) + '"]',
               '[Round "' + input('Введите номмер раунда:') + '"]',
               '[White "' + input('Введите игрока за белые фигуры:') + '"]',
               '[Black "' + input('Введите игрока за чёрные фигуры:') + '"]',
               '[Result "' + input('Введите счёт:') + '"]', '', moves]
    file_name = input('Введите название файла:')
    file = open(file_name + '.pgn', 'w')
    for i in answers:
        file.write(i + '\n')
    file.close()


def read_match():
    file_name = input('Введите название файла:')
    if '.' not in file_name:
        file_name += '.pgn'
    file = open(file_name, 'r')
    for i in range(8):
        print(file.readline().strip('[]\n'))
    previous_boards = []
    board = create_board()
    previous_boards.append(copy.deepcopy(board))
    moves = file.read().replace('\n', ' ').split()[:-1]
    file.close()
    # print(moves)
    turn = True
    for i in moves:
        if '.' in i:
            continue
        i = i.strip('+?#')
        if i == 'O-O':
            q = (0, 7)[turn]
            board[q][6] = board[q][4]
            board[q][4] = '.'
            board[q][5] = board[q][7]
            board[q][7] = '.'
            previous_boards.append(copy.deepcopy(board))
            turn = not turn
            continue
        if i == 'O-O-O':
            q = (0, 7)[turn]
            board[q][2] = board[q][4]
            board[q][4] = '.'
            board[q][3] = board[q][0]
            board[q][0] = '.'
            previous_boards.append(copy.deepcopy(board))
            turn = not turn
            continue
        i = i.replace('x', '')
        i = ('P', '')['A' <= i[0] <= 'R'] + i
        figures = figure_is_here(i[0], turn, board)
        move = [[0, 0], 0]
        move[1] = [convert_from_number(i[-1]), convert_from_alpha(i[-2])]
        if len(i) == 3:
            for k in figures:
                if possible_moves(board, [[k[0], k[1]], move[1]]):
                    move[0] = k
                    break
        else:
            if 'a' <= i[1] <= 'h':
                move[0][1] = convert_from_alpha(i[1])
                for k in figures:
                    if k[1] == move[0][1]:
                        move[0][0] = k[0]
                        break
            else:
                move[0][0] = convert_from_number(i[1])
                for k in figures:
                    if k[0] == move[0][0]:
                        move[0][1] = k[1]
                        break
        # print(i)
        # print(sfigures)
        # print(move)
        board[move[1][0]][move[1][1]] = board[move[0][0]][move[0][1]]
        board[move[0][0]][move[0][1]] = '.'
        # show_board(board)
        previous_boards.append(copy.deepcopy(board))
        turn = not turn
    show_board(board)
    now = len(previous_boards) - 1
    while True:
        # print(turn)
        i = input()
        if i == 'end':
            return
        if i == 'play' or i == 'p':
            game_process(previous_boards[now], turn, previous_boards[:now])
            return
        if i == 'forward' or i == 'f':
            if now < len(previous_boards) - 1:
                now += 1
                show_board(previous_boards[now])
                turn = not turn
        if i == 'back' or i == 'b':
            if now > 0:
                now -= 1
                show_board(previous_boards[now])
                turn = not turn
        if i == 'start' or i == 's':
            now = 0
            show_board(previous_boards[now])
            turn = True




def game_process(board, turn=True, previous_boards=[]):
    moves = ""
    move_number = 0
    # print(figure_is_here('p', True, board))
    while True:
        print(moves)
        # print(potential_moves(7, 3, board))
        show_board(board)
        move = input(("Ход чёрных:", "Ход белых:")[turn])
        if move == 'end':
            return
        if move == 'write':
            write_match(moves)
            continue
        if move == 'read':
            read_match()
            return
        move = move.lower().split()
        if len(move) != 2 or len(move[0]) != 2 or len(move[1]) != 2 or move[0][0] < 'a' or move[0][0] > 'h' or move[0][
            1] < '1' or move[0][1] > '8' or move[1][0] < 'a' or move[1][0] > 'h' or move[1][1] < '1' or move[1][
            1] > '8':
            print(message(0))
            continue
        move = [[convert_from_number(move[0][1]), convert_from_alpha(move[0][0])], [convert_from_number(move[1][1]), convert_from_alpha(move[1][0])]]
        print(move)
        if board[move[0][0]][move[0][1]] == '.':
            print(message(1))
            continue
        if (ord(board[move[0][0]][move[0][1]]) < _a) != turn:
            print(message(4))
            continue
        if same_colors(move, board):
            print(message(3))
            continue
        if possible_moves(board, move):
            if turn:
                move_number += 1
                moves += str(move_number) + ". "
            moves += journal(move, board)
            board[move[1][0]][move[1][1]] = board[move[0][0]][move[0][1]]
            board[move[0][0]][move[0][1]] = '.'
        else:
            print(message(2))
            continue
        if previous_boards.count(board) == 2:
            print(message(5))
            # print(previous_boards[-1] == board, previous_boards[-1] is board)
            return
        previous_boards.append(copy.deepcopy(board))
        # print(previous_boards.count(board))
        # print(figure_is_here(not turn, board))
        # print(figure_is_here(turn, board))
        # print(potential_cell(*figure_is_here(not turn, board), turn, board))
        if pat(not turn, board):
            print(message(6))
            return
        turn = not turn


game_process(create_board())
