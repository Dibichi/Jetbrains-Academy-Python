import random

def hof_cpu(move):
    if move == 'paper':
        return 'scissors'
    elif move == 'rock':
        return 'paper'
    elif move == 'scissors':
        return 'rock'

def all_conditions(move_one, move_two):
    ind = all_moves.index(move_one)
    other_options = all_moves[ind + 1:] + all_moves[:ind]
    losing_moves = other_options[-(len(all_moves) // 2):]
    if move_one == move_two:
        ratings[name_user] = ratings[name_user] + 50
        return f'There is a draw ({move_one})'
    else:
        if move_two in losing_moves:
            ratings[name_user] = ratings[name_user] + 100
            return f'Well done. The computer chose {move_two} and failed'
        
        else:
            return f'Sorry, but the computer chose {move_two}'

def command_handler(command):
    if command == '!exit':
        with open('rating.txt', 'w') as write_file:
            for player, score in ratings.items():
                print(player, score, file=write_file, flush=True)
                
        print('Bye!')
        exit()
    
    elif command == '!rating':
        print('Your ratings: {}'.format(str(ratings.get(name_user))))
        
def rating_reader(player):
    ratings = {}
    with open('rating.txt') as ratings_file:
        name_list = (ratings_file.read()).split('\n')
        for rate in name_list:
            name, points = rate.split()
            ratings[name[0]] = int(points)
    
    if player not in ratings:
        ratings[player] = 0

    return ratings
            
name_user = input('Enter your name:')
print(f'Hello, {name_user}')

ratings = rating_reader(name_user)

all_moves = input()
if all_moves == '':
    all_moves = ['rock', 'paper', 'scissors']
else:
    all_moves = all_moves.split(',')
    
print("Okay, let's start")

while True:
    user = input()
    if user in all_moves:
        cpu_move = random.choice(all_moves)
        print(all_conditions(user, cpu_move))
    
    elif user.startswith('!'):
        command_handler(user)
    
    else:
        print('Invalid input')
    
