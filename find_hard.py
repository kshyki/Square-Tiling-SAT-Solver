import json
import random
import time

from solver import solve_sat

COLORS = ["red", "blue", "green", "yellow"]

random.seed(42)
for k in [10, 15, 20, 25, 30]:
    for m in [8, 12, 16, 20, 24]:
        for attempt in range(100):
            tiles = [
                tuple(random.choice(COLORS) for _ in range(4))
                for _ in range(m)
            ]
            solver = solve_sat(COLORS, tiles, k)

            start = time.perf_counter()
            satisfiable = solver.solve()
            elapsed = time.perf_counter() - start

            if satisfiable and elapsed >= 10:
                instance = {
                    "colors": COLORS,
                    "tiles": tiles,
                    "k": k
                }
                with open("instances/hard_sat.json", "w") as file:
                    json.dump(instance, file, indent=4)
                print("hard sat instance:")
                print(f"k = {k}, tiles = {m}")
                solver.delete()
                raise SystemExit

            solver.delete()

print("no hard instance")