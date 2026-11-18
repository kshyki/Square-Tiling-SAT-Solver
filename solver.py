import json
from pysat.solvers import Glucose3

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
    pass

if __name__ == "__main__":
    colors, tiles, k = read_input("input.json")

    print("Colors:", colors)
    print("Tiles:", tiles)
    print("K:", k)