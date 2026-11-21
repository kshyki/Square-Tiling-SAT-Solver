# Square Tiling Problem — SAT Solver

## 1. Problem Description

The goal is to determine whether a square board of size k x k can be tiled using a given collection of coloured tiles.

### Input parameters

- C: a finite set of n colours.
- T: a collection of m tiles.
- k: the size of the square board, where 1 <= k <= n.

Each tile consists of four colours and is represented by a tuple:

t = (top, right, bottom, left)

Tiles can be used an unlimited number of times. There is no requirement to use every tile.

### Decision variables

For every board position (r,c) and every tile t in T, define a bool variable:

<img width="814" height="176" alt="image" src="https://github.com/user-attachments/assets/a372bf46-c614-466f-9641-97387e3bfd13" />

The board positions use zero-based indexing:

<img width="250" height="42" alt="image" src="https://github.com/user-attachments/assets/061116d8-1a7f-48cb-89ea-d0a2e74dc451" />

The problem is to determine whether there exists an assignment of these variables satisfying all the following constraints.

### Constraints

**1. Every cell must contain at least one tile.**

<img width="258" height="124" alt="image" src="https://github.com/user-attachments/assets/2658d6cc-abed-4674-8049-fcd5bf04ce73" />

We need to check for every cell whether it contains at least one of the tiles.

**2. Every cell must contain at most one tile.**

<img width="532" height="140" alt="image" src="https://github.com/user-attachments/assets/dc6baa7c-13e5-4ea0-acfe-367c1671349a" />

We need to check for every cell and for every pair of tiles whether at least one tile out of two is not in that cell.

**3. Horizontal compatibility.**

<img width="618" height="156" alt="image" src="https://github.com/user-attachments/assets/294c0b42-666d-482c-9e11-7612fc9e2608" />

For every pair of horizontally adjacent cells, the right side of the left tile must match the left side of the right tile.

**4. Vertical compatibility.**

<img width="654" height="184" alt="image" src="https://github.com/user-attachments/assets/e5e2ce52-f80e-4685-8ffa-016bba334beb" />

For every pair of vertically adjacent cells, the bottom side of the upper tile must match the top side of the lower tile.

---

## 2. CNF Encoding

The problem is encoded as a satisfiability problem DIMACS CNF.

The implementation uses the PySAT library and the Glucose42 SAT solver.

### Variable numbering

In order to make a CNF DIMACS format we need to translate every x[r,c,t] into a simple number. I made the following formula:

<img width="598" height="54" alt="image" src="https://github.com/user-attachments/assets/a1211b2a-f730-423f-afbf-6ab9d867664c" />

This formula represents every variable x[r,c,t] as a unique number, because after changing either the position or the tile index, the number is going to be new.

However, there is still one problem: DIMACS format uses 0 as a symbol for clause ending, so the variable index cannot be 0. Therefore, we need to add 1 to our formula, so indexing starts from 1.

Final formula:

<img width="646" height="68" alt="image" src="https://github.com/user-attachments/assets/4727c1a1-ee09-4b56-828c-8a629e1c23fe" />

## 3. User Documentation

### Requirements

- Python 3
- PySAT

Install the dependency using:

```bash
pip install python-sat
```

### Input format

The program reads an input instance from a JSON file.

The file must contain three fields:

- `colors`: an array of available colours.
- `tiles`: an array of tiles, each represented by four colours in the order `[top, right, bottom, left]`.
- `k`: the size of the square board.

Example:

```json
{
    "colors": ["red", "blue"],
    "tiles": [
        ["red", "blue", "red", "blue"]
    ],
    "k": 2
}
```

### Running the program

Run the script from the command line:

```bash
python solver.py input.json
```

Replace `input.json` with the path to the desired input file. For example of template instances:

```bash
python solver.py instances/satisfiable_instance.json
```

### Output format

The program prints either:

- `SAT` if a valid tiling exists, followed by a matrix containing the indices of the selected tiles.
- `UNSAT` if no valid tiling exists.

For example:

```text
SAT
[[0, 0],
 [0, 0]]
```

The indices in the resulting matrix are zero-based indices referring to the original `tiles` array in the input file.

Additionally, program saves the CNF DIMACS formula to file `formula.cnf`

---

## 4. Included Instances

The project includes the following test instances:

| Instance | Board size | Description | Expected result |
|---|---:|---|---|
| `satisfiable_instance.json` | 2 × 2 | Understandable example of satisfiable instance | SAT |
| `unsatisfiable_instance.json` | 2 × 2 | One tile whose horizontal and vertical sides cannot match themselves | UNSAT |
| `hard_sat.json` | 25 × 25 | An instance with solving time over 10 seconds | SAT |

---

## 5. Experiments

In order to find `hard_sat.json` I've made a script which generates random instances of tiles and tests whether their solving time is greater than 10 seconds. If so, it saves the instance to `hard_sat.json`. You can find this script as `find_hard.py`.

### Experimental Methodology

The search in `find_hard.py` is configured as follows:

- **Fixed colour palette:** `["red", "blue", "green", "yellow"]` (n = 4 colours).
- **Reproducibility:** Uses a fixed random seed (`random.seed(42)`).
- **Search grid:** Iterates over board sizes k = {10, 15, 20, 25, 30} and tile counts m = {8, 12, 16, 20, 24}, running up to `100` random attempts for each `(k, m)` pair (up to 2,500 candidate instances in total).
- **Tile generation:** Each attempt creates m tiles by sampling four colours uniformly at random with replacement for `(top, right, bottom, left)`.
- **Timing isolation:** CNF construction via `solve_sat(COLORS, tiles, k)` happens before `time.perf_counter()` starts, so only `solver.solve()` execution time is measured.
- **Stopping condition:** The first instance that is both satisfiable (`SAT`) and has `elapsed` time greater than or equal to 10 seconds is written to `hard_sat.json` (with `tiles` serialized as JSON lists) and terminates the program via `SystemExit`. If no such instance is found across the entire grid, the script prints `no hard instance`.

### Running the Search Script

Run the script from the project root:

```bash
python find_hard.py
```

Once `hard_sat.json` is generated, you can evaluate it directly with the solver:

```bash
python solver.py hard_sat.json
```
## 6. Sources

I used HostMath{https://www.hostmath.com} website to generate all the formulas.
