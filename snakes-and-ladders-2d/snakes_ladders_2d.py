"""
Snakes and Ladders variant: throw two dice, the first moves you
horizontally, the second vertically. Moves wrap around the board edges.
Snakes and ladders work as usual. You win by landing exactly on the end.

Simulates a single player's game.
"""
import random

SIZE = 10
END = SIZE * SIZE

# square -> destination; snakes go down, ladders go up
JUMPS = {
    # ladders
    4: 25, 13: 46, 33: 49, 42: 63, 50: 69, 62: 81, 74: 92,
    # snakes
    27: 5, 40: 3, 43: 18, 54: 31, 66: 45, 76: 58, 89: 53, 99: 41,
}


def to_xy(square):
    """Board square (1..100, boustrophedon) -> (x, y) with (0, 0) bottom-left."""
    y, i = divmod(square - 1, SIZE)
    return (i if y % 2 == 0 else SIZE - 1 - i), y


def to_square(x, y):
    i = x if y % 2 == 0 else SIZE - 1 - x
    return y * SIZE + i + 1


def play(rng=random, verbose=True, max_turns=None):
    """Return the number of turns taken, or None if aborted after max_turns."""
    square, turns = 1, 0
    while square != END:
        if turns == max_turns:
            return None
        turns += 1
        dx, dy = rng.randint(1, 6), rng.randint(1, 6)
        x, y = to_xy(square)
        landed = to_square((x + dx) % SIZE, (y + dy) % SIZE)
        square = JUMPS.get(landed, landed)
        if verbose:
            jump = f" -> {square}" if landed != square else ""
            print(f"Turn {turns}: rolled ({dx}, {dy}), {landed}{jump}")
    return turns


assert all(to_square(*to_xy(s)) == s for s in range(1, END + 1))

if __name__ == "__main__":
    print(f"Finished in {play()} turns")
