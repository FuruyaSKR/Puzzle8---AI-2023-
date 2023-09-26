import numpy as np
import time
import random


GOAL = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])
SOLUCION = False


def dist_manhattan(x, y):
    return sum([abs(xi - yi) for xi, yi in zip(x, y)])


def evaluation_function(state):
    h_x = 0
    g_x = 0
    for i in range(len(GOAL)):
        for j in range(len(GOAL[i])):
            if state[i][j] != GOAL[i][j] and state[i][j] != 0:
                value = state[i][j]
                goal_i, goal_j = np.where(np.array(GOAL) == value)
                h_x += dist_manhattan([i, j], [goal_i[0], goal_j[0]])
                g_x += 1
    f_x = g_x + h_x
    return f_x, g_x, h_x


def move(puzzle):
    void_position = np.where(puzzle == 0)
    v_x, v_y = void_position
    v_x = int(v_x)
    v_y = int(v_y)

    # Evaluating moves in x
    moves_x = 2 if v_x != 0 and v_x != len(puzzle) - 1 else 1
    moves_y = 2 if v_y != 0 and v_y != len(puzzle[0]) - 1 else 1

    expended_nodes = moves_x + moves_y

    possible_moves = []

    for i in range(moves_x):
        branch = puzzle.copy()
        if v_x == 0:
            branch[v_x][v_y] = puzzle[v_x + 1][v_y]
            branch[v_x + 1][v_y] = puzzle[v_x][v_y]
        elif v_x == len(puzzle) - 1:
            branch[v_x][v_y] = puzzle[v_x - 1][v_y]
            branch[v_x - 1][v_y] = puzzle[v_x][v_y]
        else:
            if i == 0:
                branch[v_x][v_y] = puzzle[v_x + 1][v_y]
                branch[v_x + 1][v_y] = puzzle[v_x][v_y]
            else:
                branch[v_x][v_y] = puzzle[v_x - 1][v_y]
                branch[v_x - 1][v_y] = puzzle[v_x][v_y]
        possible_moves.append(branch)

    for j in range(moves_y):
        branch = puzzle.copy()
        if v_y == 0:
            branch[v_x][v_y] = puzzle[v_x][v_y + 1]
            branch[v_x][v_y + 1] = puzzle[v_x][v_y]
        elif v_y == len(puzzle) - 1:
            branch[v_x][v_y] = puzzle[v_x][v_y - 1]
            branch[v_x][v_y - 1] = puzzle[v_x][v_y]
        else:
            if j == 0:
                branch[v_x][v_y] = puzzle[v_x][v_y + 1]
                branch[v_x][v_y + 1] = puzzle[v_x][v_y]
            else:
                branch[v_x][v_y] = puzzle[v_x][v_y - 1]
                branch[v_x][v_y - 1] = puzzle[v_x][v_y]
        possible_moves.append(branch)
    for index, candidate in enumerate(possible_moves):
        fx, gx, hx = evaluation_function(candidate)
        print(
            f"""
Candidate: \n{candidate}
f_x: {fx}
g_x: {gx}
h_x: {hx}
"""
        )
        print("=" * 20)
        if index == 0 or fx < best_move[1]:
            best_move = (index, fx, candidate)

    return (expended_nodes, best_move[-1])


def astar(puzzle):
    final_state = False
    total_nodes = 0
    count = 0
    while not final_state and count < 100:
        print(f"""Move: {count} \nAvaliando: \n{puzzle}""")
        nodes, puzzle = move(puzzle)
        total_nodes += nodes

        final_state = (puzzle == GOAL).all() == True
        count += 1
    SOLUCION = bool(count < 100)
    return total_nodes, puzzle


if __name__ == "__main__":
    numbers = list(range(9))
    random.shuffle(numbers)
    initial_puzzle = np.array(numbers).reshape((3, 3))
    start = time.time()
    # initial_puzzle = np.array([[2, 6, 3], [0, 1, 4], [8, 7, 5]])
    print("=" * 20)
    print(f"""Puzzle inicial:\n {initial_puzzle}\n""")
    print("=" * 20)
    total_nodes, solution = astar(initial_puzzle)
    end = time.time()
    if not SOLUCION:
        print("Nenhuma solução encontrada.")
    else:
        print("Solução encontrada:\n")
        print(solution, "\n")
    print("=" * 20)
    print(f"Nodes: {total_nodes}")
    print(f"Search time: {end-start:4f}s")
