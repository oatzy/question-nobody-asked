"""
Two-player race with the choice rules. Player 1 moves first; both start on square 1.
Optimal play maximises your chance of winning, which can depend on where your opponent
is, so we solve the zero-sum game by value iteration rather than reusing the
single-player (minimum expected turns) strategy.
"""
import random

import numpy as np

from optimal_strategy import END, INDEX, ROLLS, STATES, choices, move, optimal

GOAL = INDEX[END]


def next_states(**rules):
    """N[s, r, c]: index of the square reached from state s with roll r and choice c."""
    k = len(choices(1, 2, **rules))
    N = np.full((len(STATES), len(ROLLS), k), GOAL)
    for s in STATES:
        for r, (a, b) in enumerate(ROLLS):
            for c, d in enumerate(choices(a, b, **rules)):
                N[INDEX[s], r, c] = INDEX[move(s, *d)]
    return N


def win_probability(N, fixed=None, tol=1e-12):
    """V[me, them] = chance the player about to move wins.

    fixed: optional single-player policy as a choice index per (s, r), instead of the best.
    """
    n = len(STATES)
    V = np.full((n, n), 0.5)
    while True:
        # moving to `t` hands the turn over: I win with probability 1 - V[them, t]
        M = 1 - V.T[N]  # shape (me, roll, choice, them)
        M[N == GOAL] = 1
        best = M.max(axis=2) if fixed is None else np.take_along_axis(
            M, fixed[:, :, None, None], axis=2)[:, :, 0]
        new = best.mean(axis=1)
        new[GOAL] = 0  # unreachable as the mover (game already over)
        if np.abs(new - V).max() < tol:
            return new
        V = new


def single_player_choice(N, policy, **rules):
    """Choice index per (s, r) for a single-player policy from optimal_strategy."""
    return np.array([[choices(a, b, **rules).index(policy[s, a, b]) if s != END else 0
                      for a, b in ROLLS] for s in STATES])


def simulate(N, V, runs=100_000, seed=1):
    rng = random.Random(seed)
    wins = 0
    for _ in range(runs):
        pos, me = [INDEX[1], INDEX[1]], 0
        while True:
            r = rng.randrange(len(ROLLS))
            options = N[pos[me], r]
            if GOAL in options:
                wins += me == 0
                break
            pos[me] = min(options, key=lambda t: V[pos[1 - me], t])  # leave opponent worst off
            me = 1 - me
    return wins / runs


if __name__ == "__main__":
    start = INDEX[1]
    for name, rules in (("swap dice", dict(swap=True)),
                        ("swap dice + reverse either axis", dict(swap=True, flip_x=True, flip_y=True))):
        N = next_states(**rules)
        V = win_probability(N)
        policy, _ = optimal(**rules)
        V_single = win_probability(N, single_player_choice(N, policy, **rules))
        print(f"{name}:")
        print(f"  P(player 1 wins), both play to win:            {V[start, start]:.4f}")
        print(f"  P(player 1 wins), both use single-player play: {V_single[start, start]:.4f}")
        print(f"  simulated (100,000 games, both play to win):   {simulate(N, V):.4f}")
