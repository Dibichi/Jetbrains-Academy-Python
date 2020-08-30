import random

# Prints the board in its current state
def print_board():
    print('---------')
    for row in board:
        moves = ' '.join(row)
        print(f'| {moves} |')
    print('---------')

# Determines whos turn it is depending on the number of moves of each player
def whos_turn():
    x_list = [x_move for row in board for x_move in row if x_move == 'X']
    o_list = [o_move for row in board for o_move in row if o_move == 'O']
    if len(x_list) == len(o_list):
        return 'X'
    else:
        return 'O'

# For stage 1
def create_board():
    cells = []
    start = 0
    not_full = False

    current_board = input('Enter cells: ').replace('_', ' ')
    turn = whos_turn()
    if current_board.count(' ') > 1:
        not_full = True

    for i in range(3, 10, 3):
        row = list(current_board[start:i])
        cells.append(row)
        start = i

def copy_game_state(state):
    new_state = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
    for i in range(3):
        for j in range(3):
            new_state[i][j] = state[i][j]
    return new_state

class DefaultGame:

    def __init__(self):
        self.moves_made = {(0,0): ' ', (0, 1): ' ', (0, 2): ' ',
                           (1, 0): ' ', (1, 1): ' ', (1, 2): ' ',
                           (2, 0): ' ', (2, 1): ' ', (2, 2): ' '}
        self.turn = 'X'
        self.possible_players = {'easy': self.ai_move, 'user': self.user_move}
        self.players = {}
        self.possible_moves = None

    # Where the whole game is played
    def play_game(self, player_one, player_two):

        # Determines who the players are and what functions will be called (EX: {'X': self.ai_move})
        self.players["X"] = self.possible_players[player_one]
        self.players["O"] = self.possible_players[player_two]

        # The game - prints board, makes move, and determines if game is over
        while True:
            print_board()
            self.turn = whos_turn()
            if self.turn == 'X':
                self.players['X']()
            elif self.turn == 'O':
                self.players['O']()

            if self.game_done(board, self.turn) == 'win':
                print_board()
                print(self.turn, 'wins')
                break

            elif self.game_done(board, self.turn) == 'full':
                print_board()
                print('Tie')
                break

    # Checks if the player's move is valid
    def valid_position(self, pos):
        try:
            column = int(pos[0])
            row = int(pos[-1])
        except:
            print("You should enter numbers!")

        else:
            if not 0 < row < 4 or not 0 < column < 4:
                print("Coordinates should be from 1 to 3!")
            else:
                column = column - 1
                row = 3 - row

                if board[row][column] != ' ':
                    print('This cell is occupied! Choose another one!')

                else:
                    # Keeps track of what move is made in dict and makes it on the board
                    self.moves_made[(row, column)] = self.turn
                    board[row][column] = self.turn
                    return True

    # Checks if there is a winner or if the game is tied
    def game_done(self, the_board, current_turn):
        win = [current_turn, current_turn, current_turn]

        diagonal = [row[i] for i, row in enumerate(the_board)]
        backwards_diagonal = [row[2 - i] for i, row in enumerate(the_board)]
        # Takes the value of a column on each iteration - [0][0], [1][0]
        columns = [[row[col] for i, row in enumerate(the_board)] for col in range(3)]
        if win in board or win in columns or diagonal == win or backwards_diagonal == win:
            return 'win'

        elif len([blank for blank in self.moves_made.values() if blank == ' ']) == 0:
            return 'full'

    # Easy mode AI who moves randomly and on empty spaces
    def ai_move(self):
        self.turn = whos_turn()
        while True:
            r = random.randint(0, 2)
            c = random.randint(0, 2)
            ai_coords = (r, c)
            if self.moves_made[ai_coords] == ' ':
                board[r][c] = self.turn
                print('Making move level "easy"')
                self.moves_made[ai_coords] = self.turn
                break

    # Asks where the user wants to move and moves there
    def user_move(self):
        self.turn = whos_turn()
        while True:
            user_coords = input('Enter the coordinates: ')
            if self.valid_position(user_coords):
                break


class MediumGame(DefaultGame):

    def __init__(self):
        super().__init__()
        self.possible_players = {'easy': self.ai_move, 'medium': self.medium_move, 'user': self.user_move}
        self.possible_moves = None

    # Checks if move can win on the next move
    def can_win(self, current):
        for move in self.possible_moves:
            board[move[0]][move[1]] = current
            if self.game_done(board, current) == 'win':
                board[move[0]][move[1]] = ' '
                return move

            board[move[0]][move[1]] = ' '

    # Returns the opponent of the current turn
    def opponent(self):
        if self.turn == 'X':
            return 'O'
        else:
            return 'X'

    # Medium AI - First checks if current player can win, then checks if opponent can win, or else it makes a random move
    def medium_move(self):
        self.possible_moves = [position for position, value in self.moves_made.items() if value == ' ']
        print('Making move level "medium"')
        opponent_turn = self.opponent()

        win_move = self.can_win(self.turn)
        block_move = self.can_win(opponent_turn)

        if win_move:
            board[win_move[0]][win_move[1]] = self.turn
            self.moves_made[(win_move[0], win_move[1])] = self.turn
        elif block_move:
            board[block_move[0]][block_move[1]] = self.turn
            self.moves_made[(block_move[0], block_move[1])] = self.turn
        else:
            random_move = random.choice(self.possible_moves)
            board[random_move[0]][random_move[1]] = self.turn
            self.moves_made[(random_move[0], random_move[1])] = self.turn


class HardGame(MediumGame):
    def __init__(self):
        super().__init__()
        self.possible_players = {'easy': self.ai_move, 'medium': self.medium_move, 'hard': self.hard_move, 'user': self.user_move}
        self.opponent_turn = None

    # The minimax algorithm - PAIN
    def minimax(self, current_turn):
        # Finds all possible moves on board
        global board

        # Base case
        # None is used here so result[0] can be used w/o error
        if self.game_done(board, self.opponent_turn) == 'win':
            return -1, None
        elif self.game_done(board, self.turn) == 'win':
            return 1, None
        elif self.game_done(board, current_turn) == 'full':
            return 0, None

        moves = []
        # Goes through all possible moves and assigns a score
        for x,row in enumerate(board):
            for y,val in enumerate(row):
                if val == ' ':
                    board[x][y] = current_turn
                    self.moves_made[x, y] = current_turn

                    if self.opponent_turn == current_turn:
                        result = self.minimax(self.turn)
                    else:
                        result = self.minimax(self.opponent_turn)

                    # Will only take the first value of return - -1, 1, 0
                    # and excludes the None and tuple of coordinates which prevents messing up moves
                    move = (result[0], (x,y))
                    board[x][y] = ' '
                    self.moves_made[x, y] = ' '

                    moves.append(move)

        # Calculates the theoretical best move
        return min(moves) if current_turn == self.opponent_turn else max(moves)

    # Makes the best move possible based on the minimax algorithm
    def hard_move(self):
        self.opponent_turn = self.opponent()
        best = self.minimax(self.turn)[1]
        board[best[0]][best[1]] = self.turn
        self.moves_made[best[0], best[1]] = self.turn
        print('Making move level "hard"')


difficulties = ['user', 'easy', 'medium', 'hard']
while True:
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    try:
        user_game = input('Input command: ').split()
        if user_game[0] == 'exit':
            exit()

        # What difficulty the game will be in
        elif user_game[0] == 'start' and (user_game[1] in difficulties) and (user_game[2] in difficulties):
            if 'hard' in user_game:
                game = HardGame()

            elif 'medium' in user_game:
                game = MediumGame()

            else:
                game = DefaultGame()

            game.play_game(user_game[1], user_game[2])

        else:
            print('Bad parameters!')

    except IndexError:
        print('Bad parameters!')

