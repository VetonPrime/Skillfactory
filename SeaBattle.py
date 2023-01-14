import random


class BoardOutException:
    pass


class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


class Ship:

    def __init__(self, length, dot, horizontal):
        self.length = length
        self.dot = dot
        self.horizontal = horizontal
        self.lives = length

    def dots(self):
        list_dots = list()
        list_dots.append(self.dot)
        for i in range(1, self.length):
            if self.horizontal:
                list_dots.append(Dot(self.dot.x+i, self.dot.y))
            else:
                list_dots.append(Dot(self.dot.x, self.dot.y+i))
        return list_dots


class Board:
    count_ships = 0

    def __init__(self, hid, field_size=6):
        self.list_ships = []
        self.list_shots = []
        self.hid = hid
        self.battle_field = [['O' for _ in range(field_size + 1)] for _ in range(field_size + 1)]
        for line in range(len(self.battle_field)):
            for row in range(len(self.battle_field)):
                if not (line or row):
                    self.battle_field[line][row] = ' '
                elif not (line and row):
                    self.battle_field[line][row] = str(line + row)

    def add_ship(self, ship):
        self.list_ships.append(ship)
        for dot in ship.dots():
            self.battle_field[dot.x][dot.y] = '■'
            self.contour(ship)

    def contour(self, ship):
        for dot in ship.dots():
            for i in range(3):
                for j in range(3):
                    x = min(dot.x + i - 1, len(self.battle_field)-1)
                    y = min(dot.y + j - 1, len(self.battle_field)-1)
                    if self.battle_field[x][y] == 'O':
                        self.battle_field[x][y] = '•'

    def out(self, dot):
        return not (0 < dot.x <= len(self.battle_field)-1 and 0 < dot.y <= len(self.battle_field)-1)

    def shot(self, dot):
        repeat_shot = False
        if self.out(dot):
            print('Точка за пределами поля. Повторите ход')
            repeat_shot = True
        elif dot in self.list_shots:
            print('Вы уже стреляли в эту точку. Повторите ход')
            repeat_shot = True
        else:
            self.list_shots.append(dot)
            self.battle_field[dot.x][dot.y] = '•'
            for ship in self.list_ships:
                ship_dots = ship.dots()
                for ship_dot in ship_dots:
                    if dot == ship_dot:
                        self.battle_field[dot.x][dot.y] = 'X'
                        ship.lives -= 1
                        if ship.lives == 0:
                            self.list_ships.remove(ship)
                            self.contour(ship)
                            print('Убил! Снова ваш ход.')
                        else:
                            print('Ранил! Снова ваш ход.')
                        repeat_shot = len(self.list_ships) != 0

        return repeat_shot


class Player:
    def __init__(self, board_player, board_opponent):
        self.board_player = board_player
        self.board_opponent = board_opponent

    def ask(self):
        pass

    def move(self):
        try:
            dot = self.ask()
        except BoardOutException:
            print('Точка находится за пределами игровой доски. Повторите попытку')
        else:
            return self.board_opponent.shot(dot)

    def __str__(self):
        res = ''
        for i in range(len(self.board_player.battle_field)):
            res += ' | '.join(self.board_player.battle_field[i]) + '\t' * 3 \
                   + ' | '.join(self.board_opponent.battle_field[i]).replace('■', 'O') + '\n'
        return res


class AI(Player):
    def ask(self):
        x = random.randint(1, len(self.board_opponent.battle_field)-1)
        y = random.randint(1, len(self.board_opponent.battle_field)-1)
        print(f'ИИ походил {x} {y} ')
        return Dot(x, y)


class User(Player):
    def ask(self):
        while True:
            try:
                x, y = map(int, input('Введите через пробел номер строки и столбца, куда хотите стрелять: ').split())
            except ValueError:
                print('Вы ввели некоректные значения, повторите ввод!')
            else:
                return Dot(x, y)


class Game:
    def __init__(self):
        self.board_user = Board(False)
        self.board_ai = Board(True)

        while True:
            self.random_board(self.board_user)
            self.random_board(self.board_ai)
            if len(self.board_user.list_ships) == 6 and len(self.board_ai.list_ships) == 6:
                break

        self.player_user = User(self.board_user, self.board_ai)
        self.player_ai = AI(self.board_ai, self.board_user)

    @staticmethod
    def random_board(board):
        list_ships = [3, 2, 2, 1, 1, 1]
        count = 0
        for el_ship in list_ships:
            while True:
                count += 1
                x = random.randint(1, len(board.battle_field)-1)
                y = random.randint(1, len(board.battle_field)-1)
                dot = Dot(x, y)
                ship = Ship(el_ship, dot, random.randint(0, 1))
                all_dots_correct = True
                for dot in ship.dots():
                    if board.out(dot) or board.battle_field[dot.x][dot.y] != 'O':
                        all_dots_correct = False
                if all_dots_correct:
                    board.add_ship(ship)
                    break
                if count > 2000:
                    break

        for line in range(len(board.battle_field)):
            for row in range(len(board.battle_field)):
                if board.battle_field[line][row] == '•':
                    board.battle_field[line][row] = 'O'

    @staticmethod
    def greet():
        print('Добро пожаловать в игру!!')
        print('Давай поиграем!')

    def loop(self):
        user_turn = True
        run_game = True
        while run_game:
            repeat_shot = True
            while repeat_shot:
                if user_turn:
                    print(self.player_user)
                    repeat_shot = self.player_user.move()
                else:
                    repeat_shot = self.player_ai.move()

            user_turn = not user_turn

            if len(self.board_ai.list_ships) == 0:
                print('Победил человек!!')
                run_game = False
            elif len(self.board_user.list_ships) == 0:
                print('Победил компьютер!!')
                run_game = False

            if not run_game:
                print(self.player_user)

    def start(self):
        self.greet()
        self.loop()


new_game = Game()
new_game.start()
