"""Run the 2D Snakes and Ladders game many times and show the turn distribution."""
import statistics
from collections import Counter

from snakes_ladders_2d import play

RUNS = 10_000
MAX_TURNS = 1000
BIN = 50

results = [play(verbose=False, max_turns=MAX_TURNS) for _ in range(RUNS)]
turns = sorted(t for t in results if t is not None)
aborted = RUNS - len(turns)

print(f"Runs: {RUNS}, finished: {len(turns)}, aborted (>{MAX_TURNS} turns): {aborted}")
print(f"Min {turns[0]}, max {turns[-1]}, mean {statistics.mean(turns):.1f}, "
      f"median {statistics.median(turns)}")
q = statistics.quantiles(turns, n=100)
print(f"10th pct {q[9]:.0f}, 90th pct {q[89]:.0f}, 99th pct {q[98]:.0f}\n")

bins = Counter(t // BIN for t in turns)
peak = max(bins.values())
for b in range(MAX_TURNS // BIN):
    n = bins[b]
    print(f"{b * BIN + 1:4}-{(b + 1) * BIN:4} | {'#' * round(60 * n / peak):60} {n}")
