import numpy as np
import time
import random
from puzzle import Puzzle
from GeneratePuzzle import GeneratePuzzle


GOAL = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])
SOLUTION = False
iter_limit = 100
final_state = False


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
        # print("=" * 20)
        # if index == 0 or fx < best_move[1]:
        #     best_move = (index, fx, candidate)

    # TODO [X] passar todos os candidatos
    return (expended_nodes, possible_moves)


def astar(puzzle):
    total_nodes = 0
    count = 0
    global final_state
    fx, _, _ = evaluation_function(puzzle)
    open_list = [(puzzle, fx, 0)]
    black_list = []
    while True:
        puzzle, fx, parent = open_list[0]
        print(f"""Move: {count} \nAvaliando: \n{puzzle}""")
        # TODO [X] verificar se o fx == 0 [break]
        # TODO [X] Adicionar o puzzle analisado na black_list
        # TODO [X]remover o puzzle da open_list
        if fx == 0:
            final_state = True
            break
        else:
            black_list.append((puzzle, fx, parent))
            open_list.remove((puzzle, fx, parent))

        nodes, candidates = move(puzzle)

        # TODO [X] verificar se algum candidato ta na black_list
        # TODO [X] adicionar os candidatos na open_list
        for puz in candidates:
            founded = False
            for item in black_list:
                if (puz == item[0]).all():
                    candidates = [x for x in candidates if not (x == item[0]).all()]
                    founded = True
                    continue
            if not founded:
                fx, _, _ = evaluation_function(puz)
                open_list.append((puz, fx, puzzle))

        # TODO [X] fazer um sort da open_list pelo fx
        open_list = sorted(open_list, key=lambda x: x[1])

        total_nodes += nodes

        final_state = (puzzle == GOAL).all() == True
        count += 1
    # SOLUTION = bool(count < iter_limit)
    parent = open_list[0][-1]
    route_to_goal = [open_list[0][0], open_list[0][-1]]
    while type(parent) != int:
        route_to_goal.append(
            [item[-1] for item in black_list if (item[0] == parent).all()][0]
        )
        parent = route_to_goal[-1]
    return total_nodes, open_list[0][0], route_to_goal


if __name__ == "__main__":
    numbers = list(range(9))
    start = time.time()
    # initial_puzzle = np.array([[0, 2, 7], [6, 4, 1], [5, 3, 8]])
    initial_puzzle = GeneratePuzzle(None).generate_puzzle()
    print("=" * 20)
    print(f"""Puzzle inicial:\n {initial_puzzle}\n""")
    print("=" * 20)
    with open("testando.txt", "w") as f:
        f.write(f"{initial_puzzle}")
    total_nodes, solution, route = astar(initial_puzzle)
    end = time.time()
    if not final_state:
        print("Nenhuma solução encontrada.")
    else:
        print("Solução encontrada:\n")
        print(solution, "\n")
    print("=" * 20)
    print(f"Nodes: {total_nodes}")
    print(f"Search time: {end-start:4f}s")

    if final_state:
        # TODO [X]refazer o route baseado nos pais da resposta final
        route = route[::-1][1:]
        route = [[num for row in step for num in row] for step in route]
        Puzzle(route).initialization()
