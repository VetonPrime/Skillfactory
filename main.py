import random

# Подготовим игровую доску
size = 3
opponent_ai = False

second_player = input('С кем играем? (1 - ИИ, 2 - второй игрок): ')
if second_player in ['1', '2']:
    opponent_ai = (second_player == '1')
else:
    print('Некорректный выбор второго игрока')
    exit()

game_board = [['-' for i in range(size + 1)] for j in range(size + 1)]

for i in range(len(game_board)):
    for j in range(len(game_board[i])):
        if not(i or j):
            game_board[i][j] = ''
        elif not(i and j):
            game_board[i][j] = str(i + j)

for i in game_board:
    print('\t'.join(map(str, i)))


def make_move():

    result = False
    if game_board[x][y] == '-':
        game_board[x][y] = 'X' if is_first_player else 'O'
        result = True
    else:
        print('Указанная клетка уже занята!')

    print()
    for i in game_board:
        print('\t'.join(map(str, i)))

    return result


def check_for_victory():
    a = 'X' if is_first_player else 'O'
    for i in range(1, len(game_board)):
        for j in range(1, len(game_board)):
            if game_board[i][j] == a:
                if any([
                    i < size and game_board[i - 1][j] == a and game_board[i + 1][j] == a,
                    j < size and game_board[i][j - 1] == a and game_board[i][j + 1] == a,
                    i < size and j < size and game_board[i - 1][j - 1] == a and game_board[i + 1][j + 1] == a,
                    i < size and j < size and game_board[i - 1][j + 1] == a and game_board[i + 1][j - 1] == a
                ]):
                    return True
    return False


count_moves = size ** 2
is_first_player = True
while count_moves > 0:

    if opponent_ai and not is_first_player:
        while True:
            x, y = random.randint(1, size), random.randint(1, size)
            if game_board[x][y] == '-':
                break
    else:
        try:
            x, y = map(int, input('Введите через пробел номер строки и колонки: ').split())
            if not (0 < x <= size and 0 < y <= size):
                print('Указанная клетка находится за пределами игровой доски. Попробуйте ещё раз\n')
                continue

        except ValueError:
            print('Вы ввели некорректные значения! Попробуйте ещё раз\n')
            continue

    move_is_made = make_move()
    if move_is_made:

        player_win = check_for_victory()
        if player_win:

            if is_first_player:
                winner = 'Первый игрок'
            elif opponent_ai:
                winner = 'Искусственный интеллект'
            else:
                winner = 'Второй игрок'

            print(f'{winner} победил!!')
            break
        else:
            is_first_player = not is_first_player

        count_moves -= 1
        # Проверим остались ли ещё ходы
        if count_moves == 0:
            print('Ничья!!')
