import random


def print_board(board):
    for i in range(0, 3):
        if i % 1 == 0 and i != 0:
            print("-+-+-")
        for j in range(0, 3):
            if j % 1 == 0 and j != 0:
                print("|", end="")
            print(board[i][j], end="")
        print()


def user_move(board, symbol):
    while True:
        user_input = input("Where do you want to play? Choose: (1-9) ")
        if is_valid_move(board, user_input):
            break
        else:
            print(user_input + " is an invalid move... Please select a valid move.")
    place_move(board, user_input, symbol)


def computer_move(board, symbol):
    while True:
        computer_turn_number = random.randrange(0, 9) + 1
        if is_valid_move(board, str(computer_turn_number)):
            break
    place_move(board, str(computer_turn_number), symbol)


def is_valid_move(board, position):
    if position == '1':
        return board[0][0] == ' '
    elif position == '2':
        return board[0][1] == ' '
    elif position == '3':
        return board[0][2] == ' '
    elif position == '4':
        return board[1][0] == ' '
    elif position == '5':
        return board[1][1] == ' '
    elif position == '6':
        return board[1][2] == ' '
    elif position == '7':
        return board[2][0] == ' '
    elif position == '8':
        return board[2][1] == ' '
    elif position == '9':
        return board[2][2] == ' '
    else:
        return False


def place_move(board, user_input, selection_symbol):
    if user_input == '1':
        board[0][0] = selection_symbol
    elif user_input == '2':
        board[0][1] = selection_symbol
    elif user_input == '3':
        board[0][2] = selection_symbol
    elif user_input == '4':
        board[1][0] = selection_symbol
    elif user_input == '5':
        board[1][1] = selection_symbol
    elif user_input == '6':
        board[1][2] = selection_symbol
    elif user_input == '7':
        board[2][0] = selection_symbol
    elif user_input == '8':
        board[2][1] = selection_symbol
    elif user_input == '9':
        board[2][2] = selection_symbol
    else:
        print("Not a valid input, Select a valid input")


def is_game_finished(board, current_player):
    if has_contestant_won(board, current_player):
        return True

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                return False
    return True


def has_contestant_won(board, selection_symbol):
    if ((board[0][0] == selection_symbol and board[0][1] == selection_symbol and board[0][2] == selection_symbol) or
            (board[1][0] == selection_symbol and board[1][1] == selection_symbol and board[1][2] == selection_symbol) or
            (board[2][0] == selection_symbol and board[2][1] == selection_symbol and board[2][2] == selection_symbol) or
            (board[0][0] == selection_symbol and board[1][0] == selection_symbol and board[2][0] == selection_symbol) or
            (board[0][1] == selection_symbol and board[1][1] == selection_symbol and board[2][1] == selection_symbol) or
            (board[0][2] == selection_symbol and board[1][2] == selection_symbol and board[2][2] == selection_symbol) or
            (board[0][0] == selection_symbol and board[1][1] == selection_symbol and board[2][2] == selection_symbol) or
            (board[0][2] == selection_symbol and board[1][1] == selection_symbol and board[2][0] == selection_symbol)):
        return True
    return False
