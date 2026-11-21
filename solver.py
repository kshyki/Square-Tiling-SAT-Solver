import json
import argparse
from pysat.solvers import Glucose42
from pysat.formula import CNF

SIDE = {"LEFT" : 3,
        "TOP" : 0,
        "RIGHT" : 1,
        "BOTTOM" : 2}

def hashing(row, col, index, size, tilesNumber):
    return (row * size + col) * tilesNumber + index + 1

def read_input(filename):
    with open(filename, "r") as file:
        data = json.load(file)

        colors = data["colors"]
        tiles = data["tiles"]
        k = data["k"]

        tiles = list(map(tuple, tiles))

    if not validation(colors, tiles, k):
        raise ValueError("Invalid input data")

    return colors, tiles, k

def validation(colors, tiles, k):
    if len(set(colors)) != len(colors) or len(colors) < 1:
        return False

    if len(tiles) < 1:
        return False

    for tile in tiles:
        if len(tile) != 4:
            return False
        for color in tile:
            if color not in colors:
                return False

    if k < 1:
        return False

    if k > len(colors):
        return False

    return True

def solve_sat(colors, tiles, k):
    solver = Glucose42()
    m = len(tiles)
    cnf = CNF()

    for row in range(k):
        for col in range(k):

            cnf.append([hashing(row, col, i, k, m) for i in range(m)])

            for p in range(m):
                for q in range(p + 1, m):
                    clause = [
                        -hashing(row, col, p, k, m),
                        -hashing(row, col, q, k, m)
                    ]

                    cnf.append(clause)

    for row in range(k):
        for col in range(k - 1):
            for p in range(m):
                for q in range(m):
                    if tiles[p][SIDE["RIGHT"]] != tiles[q][SIDE["LEFT"]]:
                        cnf.append([
                            -hashing(row, col, p, k, m),
                            -hashing(row, col + 1, q, k, m)
                        ])

    for row in range(k-1):
        for col in range(k):
            for p in range(m):
                for q in range(m):
                    if tiles[p][SIDE["BOTTOM"]] != tiles[q][SIDE["TOP"]]:
                        cnf.append([
                            -hashing(row, col, p, k, m),
                            -hashing(row + 1, col, q, k, m)
                        ])
    cnf.to_file("formula.cnf")
    solver = Glucose42(bootstrap_with=cnf.clauses)
    return solver

def decode(model, k, m):
    board = []
    true_variables = {x for x in model if x > 0}

    for row in range(k):
        current_row = []

        for col in range(k):
            for t in range(m):
                variable = hashing(row, col, t, k, m)

                if variable in true_variables:
                    current_row.append(t)
                    break

        board.append(current_row)

    return board

def print_results(board):
    for row in board:
        print(row)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="Path to input JSON file")
    args = parser.parse_args()
    colors, tiles, k = read_input(args.input)

    solver = solve_sat(colors, tiles, k)

    if solver.solve():
        print("SAT")
        model = solver.get_model()
        board = decode(model, k, len(tiles))
        print_results(board)
    else:
        print("UNSAT")

    solver.delete()