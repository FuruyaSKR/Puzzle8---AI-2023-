from heapq import heappop, heappush
import math
import numpy as np
import time
import random
import heapq


def f_x(puzzle):
    return g_x(puzzle) + h_x(puzzle)


def g_x(puzzle):
    goal = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])
    count = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != goal[i][j]:
                count += puzzle[i][j]
    return count


def h_x(puzzle):
    goal = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])
    distance = 0
    for i in range(3):
        for j in range(3):
            if puzzle[i][j] != goal[i][j]:
                value = puzzle[i][j]
                goal_i, goal_j = np.where(np.array(goal) == value)
                distance += dist_manhattan([i, j], [goal_i[0], goal_j[0]])
    return distance


def dist_manhattan(x, y):
    return sum([abs(xi - yi) for xi, yi in zip(x, y)])


# def move_piece(puzzle, move):
#     empty_i, empty_j = np.where(np.array(puzzle) == 0)

#     if move == "cima":
#         if empty_i > 0:
#             puzzle[empty_i][empty_j], puzzle[empty_i - 1][empty_j] = (
#                 puzzle[empty_i - 1][empty_j],
#                 puzzle[empty_i][empty_j],
#             )
#     elif move == "baixo":
#         if empty_i < 2:
#             puzzle[empty_i][empty_j], puzzle[empty_i + 1][empty_j] = (
#                 puzzle[empty_i + 1][empty_j],
#                 puzzle[empty_i][empty_j],
#             )
#     elif move == "esquerda":
#         if empty_j > 0:
#             puzzle[empty_i][empty_j], puzzle[empty_i][empty_j - 1] = (
#                 puzzle[empty_i][empty_j - 1],
#                 puzzle[empty_i][empty_j],
#             )
#     elif move == "direita":
#         if empty_j < 2:
#             puzzle[empty_i][empty_j], puzzle[empty_i][empty_j + 1] = (
#                 puzzle[empty_i][empty_j + 1],
#                 puzzle[empty_i][empty_j],
#             )

#     return puzzle


def move_function(puzzle):
    empty_tile = np.where(puzzle == 0)
    empty_i, empty_j = empty_tile[0][0], empty_tile[1][0]

    moves = []
    if empty_i > 0:
        new_puzzle = puzzle.copy()
        new_puzzle[empty_i, empty_j] = new_puzzle[empty_i - 1, empty_j]
        new_puzzle[empty_i - 1, empty_j] = 0
        moves.append(new_puzzle)

    if empty_i < 2:
        new_puzzle = puzzle.copy()
        new_puzzle[empty_i, empty_j] = new_puzzle[empty_i + 1, empty_j]
        new_puzzle[empty_i + 1, empty_j] = 0
        moves.append(new_puzzle)

    if empty_j > 0:
        new_puzzle = puzzle.copy()
        new_puzzle[empty_i, empty_j] = new_puzzle[empty_i, empty_j - 1]
        new_puzzle[empty_i, empty_j - 1] = 0
        moves.append(new_puzzle)

    if empty_j < 2:
        new_puzzle = puzzle.copy()
        new_puzzle[empty_i, empty_j] = new_puzzle[empty_i, empty_j + 1]
        new_puzzle[empty_i, empty_j + 1] = 0
        moves.append(new_puzzle)

    return moves


def astar(puzzle):
    # Inicialização
    open_set = []
    closed_set = set()
    heapq.heappush(open_set, (f_x(puzzle), puzzle))

    while open_set:
        # Seleciona o estado com menor valor de f_x()
        current_state = heapq.heappop(open_set)[1]

        # Verifica se é o estado objetivo
        if is_goal_state(current_state):
            return current_state

        # Adiciona o estado atual ao conjunto fechado
        closed_set.add(tuple(map(tuple, current_state)))

        # Gera os possíveis movimentos
        moves = move_function(current_state)

        for move in moves:
            # Verifica se o estado já foi visitado
            if tuple(map(tuple, move)) in closed_set:
                continue

            # Calcula os valores f_x(), g_x() e h_x() para o novo estado
            f = f_x(move)
            g = g_x(move)
            h = h_x(move)
            print(f"Função de g_x(): {g}, Função de h_x(): {h}")
            # Adiciona o novo estado à lista de estados abertos
            heapq.heappush(open_set, (f, move))

    return None


def is_goal_state(puzzle):
    goal = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])
    return np.array_equal(puzzle, goal)


def main():
    start_time = time.time()

    numbers = list(range(9))
    random.shuffle(numbers)
    puzzle = np.array(numbers).reshape((3, 3))

    goal = np.array([[1, 2, 3], [8, 0, 4], [7, 6, 5]])
    num_nodes = 0

    while not np.array_equal(puzzle, goal):
        # Escolha um movimento aleatório
        moves = ["cima", "baixo", "esquerda", "direita"]
        move = random.choice(moves)

        # Faça o movimento escolhido
        puzzle = move_piece(puzzle, move)

        # Incremente o número de nodos na árvore de busca
        num_nodes += 1

        # Imprima os resultados
        print(f"Quebra-cabeça resolvido em {num_nodes} nodos.")

    # Adicione o timer para verificar o tempo de execução
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tempo de execução: {execution_time} segundos")


if __name__ == "__main__":
    numbers = list(range(9))
    random.shuffle(numbers)
    initial_puzzle = np.array(numbers).reshape((3, 3))
    solution = astar(initial_puzzle)

    if solution is None:
        print("Nenhuma solução encontrada.")
    else:
        print("Solução encontrada:")
        print(solution)
