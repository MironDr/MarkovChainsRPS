import random

import numpy as np

import matplotlib.pyplot as plt

prev_move = ''

moves = ['r', 'p', 's']

transition_map = {
    'r': {'r': 1, 'p': 1, 's': 1},
    'p': {'r': 1, 'p': 1, 's': 1},
    's': {'r': 1, 'p': 1, 's': 1}
}


def get_sty_by_int(move_int):
    global moves
    return moves[move_int] if 0 <= move_int < 3 else None


def rock_paper_scissors(player_move, computer_move):
    if (player_move == 'r' and computer_move == 's') or \
            (player_move == 's' and computer_move == 'p') or \
            (player_move == 'p' and computer_move == 'r'):
        return 1

    elif (computer_move == 'r' and player_move == 's') or \
            (computer_move == 's' and player_move == 'p') or \
            (computer_move == 'p' and player_move == 'r'):
        return -1

    else:
        return 0


def update_transition_map(current_move):
    global transition_map
    global prev_move
    if prev_move is not None and prev_move != '':
        transition_map[prev_move][current_move] += 1
    prev_move = current_move


def counter_move(move):
    if move == 'r':
        return 'p'
    elif move == 'p':
        return 's'
    elif move == 's':
        return 'r'
    else:
        return None


def choose_move():
    global transition_map
    global prev_move
    if prev_move == '':
        return get_sty_by_int(random.randint(0, 2))
    else:
        current_row = transition_map[prev_move]
        counts = np.array([current_row['r'], current_row['p'], current_row['s']])
        max_count = np.max(counts)
        maxes = (counts == max_count)
        filtered_row = counts * maxes
        probabilities = filtered_row / np.sum(filtered_row)
        return counter_move(np.random.choice(moves, p=probabilities))



def play_game():
    global prev_move
    print("Game: Rock (r), Paper (p), Scissors (s). Enter 'q' to quit.")
    history = []

    while True:
        player_move = input("Your move (r/p/s): ").strip().lower()
        if player_move == 'q':
            print("Exiting the game.")
            break
        if player_move not in moves:
            print("Invalid input. Enter 'r', 'p', or 's'.")
            continue

        make_move(player_move, history)

    plt.plot(history)
    plt.ylabel('results')
    plt.savefig('plot.png')


def make_move(move, history):
    computer_move = choose_move()
    result = rock_paper_scissors(move, computer_move)
    update_transition_map(move)
    prev_result = 0
    print(f"Computer chose: {computer_move}")

    if len(history) > 0:
        prev_result = history[len(history) - 1]

    if result == 1:
        print("You won!")
        history.append(prev_result + result)
    elif result == -1:
        print("You lost!")
        history.append(prev_result + result)
    else:
        print("It's a draw!")
        history.append(prev_result + result)


def simulate_games(n):
    history = []

    for _ in range(n):
        player_move = random.choice(moves)
        make_move(player_move, history)

    print(f"Simulation of {n} games completed:")
    plt.plot(history)
    plt.ylabel('results')
    plt.savefig('plot.png')


play_game()
