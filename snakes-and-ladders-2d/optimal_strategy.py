"""
Variant: after throwing, you choose which die is horizontal and which is vertical.
Find the strategy minimising the expected number of turns, using policy iteration
over the exact Markov chain, and compare it with simpler strategies.
"""
import random
import statistics

import numpy as np

from snakes_ladders_2d import END, JUMPS, SIZE, play, to_square, to_xy

ROLLS = [(a, b) for a in range(1, 7) for b in range(1, 7)]
# squares you can actually stand on (never the bottom of a ladder / head of a snake)
STATES = [s for s in range(1, END + 1) if s not in JUMPS]
INDEX = {s: i for i, s in enumerate(STATES)}


def move(square, dx, dy):
    x, y = to_xy(square)
    landed = to_square((x + dx) % SIZE, (y + dy) % SIZE)
    return JUMPS.get(landed, landed)


def evaluate(policy):
    """Exact expected turns from each square. policy[(square, a, b)] -> (dx, dy)."""
    n = len(STATES)
    P = np.zeros((n, n))
    for s in STATES:
        if s == END:
            continue
        for a, b in ROLLS:
            P[INDEX[s], INDEX[move(s, *policy[s, a, b])]] += 1 / len(ROLLS)
    A = np.eye(n) - P
    rhs = np.ones(n)
    A[INDEX[END]], rhs[INDEX[END]] = 0, 0  # E[END] = 0
    A[INDEX[END], INDEX[END]] = 1
    E = np.linalg.solve(A, rhs)
    return {s: E[INDEX[s]] for s in STATES}


def make_policy(pick):
    return {(s, a, b): pick(s, a, b) for s in STATES for a, b in ROLLS}


def optimal():
    policy = make_policy(lambda s, a, b: (a, b))
    while True:
        E = evaluate(policy)
        better = make_policy(
            lambda s, a, b: min((a, b), (b, a), key=lambda d: (E[move(s, *d)], d != policy[s, a, b]))
        )
        if better == policy:
            return policy, E
        policy = better


def higher_square(s, a, b):
    """Naive: take whichever lands on the higher-numbered square (after snakes/ladders)."""
    return max((a, b), (b, a), key=lambda d: move(s, *d) % END if move(s, *d) != END else END)


def in_launch_zone(square):
    """Squares from which 100 (x=0, y=9) is reachable in one throw: both offsets in 1..6."""
    x, y = to_xy(square)
    return 4 <= x <= 9 and 3 <= y <= 8


def launch_zone(s, a, b):
    """Human-friendly: win if you can, else land in the launch zone if you can."""
    options = [(a, b), (b, a)]
    for test in (lambda t: t == END, in_launch_zone):
        for d in options:
            if test(move(s, *d)):
                return d
    return a, b


def simulate(policy, runs=10_000):
    rng = random.Random(1)
    return [play(rng, verbose=False, choose=lambda s, a, b: policy[s, a, b]) for _ in range(runs)]


if __name__ == "__main__":
    best, E_best = optimal()
    strategies = {
        "fixed (first die horizontal)": make_policy(lambda s, a, b: (a, b)),
        "higher square": make_policy(higher_square),
        "launch zone": make_policy(launch_zone),
        "optimal": best,
    }
    for name, policy in strategies.items():
        print(f"{name:30} expected turns from start: {evaluate(policy)[1]:6.2f}")

    turns = simulate(best)
    print(f"\nSimulated optimal (10,000 runs): mean {statistics.mean(turns):.1f}, "
          f"median {statistics.median(turns)}")

    print("\nExpected turns remaining under optimal play (board as drawn, 100 top-left):")
    for y in reversed(range(SIZE)):
        row = []
        for x in range(SIZE):
            s = to_square(x, y)
            row.append(f"{'  --' if s in JUMPS else f'{E_best[s]:4.0f}'}")
        print(" ".join(row))
