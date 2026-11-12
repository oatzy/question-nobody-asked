# 2D Snakes and Ladders

A variation on Snakes and Ladders where you throw two dice: the first moves you
horizontally, the second vertically. Moves that go off the edge of the board wrap
around. Snakes and ladders work as usual, and you win by landing exactly on the end
square.

## Assumptions

- 10×10 board, squares numbered 1–100 in the usual zig-zag (boustrophedon) layout.
- Movement is always right (+x) and up (+y), regardless of the row's numbering direction.
- The player starts on square 1.
- Snake and ladder positions are made up (see `JUMPS` in `snakes_ladders_2d.py`).
- Since moves wrap, you can't overshoot, so "exactly" just means landing on 100.

## Scripts

- `snakes_ladders_2d.py`: simulates a single game, printing each turn.
- `distribution.py`: runs 10,000 games (each aborted after 1,000 turns) and prints
  the distribution of turns taken.
- `optimal_strategy.py`: the "choose your dice" variant (see below). Requires numpy.

## Results

From one run of `distribution.py` (unseeded, so the numbers vary slightly between runs):

- Runs: 10,000, all finished (none hit the 1,000-turn limit)
- Min 2, max 835, mean 100.6, median 71
- 10th percentile 12, 90th percentile 231, 99th percentile 462

```
   1-  50 | ############################################################ 3848
  51- 100 | ######################################                       2408
 101- 150 | #######################                                      1506
 151- 200 | ##############                                               902
 201- 250 | ########                                                     514
 251- 300 | #####                                                        341
 301- 350 | ###                                                          192
 351- 400 | ##                                                           106
 401- 450 | #                                                            68
 451- 500 | #                                                            44
 501- 550 |                                                              30
 551- 600 |                                                              19
 601- 650 |                                                              5
 651- 700 |                                                              5
 701- 750 |                                                              3
 751- 800 |                                                              8
 801- 850 |                                                              1
 851-1000 |                                                              0
```

The distribution decays roughly geometrically, which suggests each turn has a similar
chance of hitting square 100 wherever you are. In this variant, winning is mostly luck.

## Variant: choose which die is horizontal

After throwing, you choose which die is the horizontal move and which is the vertical.

`optimal_strategy.py` computes the exact expected number of turns for a strategy by
solving the game's Markov chain, and finds the optimal strategy by policy iteration.
This is optimal for this particular snake and ladder layout only.

| Strategy | Expected turns |
|---|---|
| No choice (first die always horizontal) | 100.8 |
| Take whichever move lands on the higher square | 52.2 |
| Launch zone rule (below) | 40.7 |
| Optimal | 37.7 |

### The launch zone rule

1. If either way round lands you on 100, take it.
2. Otherwise, if either way round lands you in the launch zone, take it.
3. Otherwise, it doesn't matter much.

The launch zone is the 6×6 block of squares from which 100 can be reached in one throw
(29 squares once snakes and ladders are excluded). Since each die moves at most 6,
nowhere else can reach the end directly.

### Why choosing helps

With no choice, the game is mostly waiting for one exact roll. With a choice, any roll
where the dice differ gives two chances to hit 100, and you can use the choice to stay
in the launch zone between throws. Under optimal play, the expected turns remaining is
about 36 to 38 from almost every square, so where you are matters little as long as you
can get back into the zone.

### Checks

- The exact expected turns with no choice (100.8) matches the simulated mean above (100.6).
- 10,000 simulated games with the optimal strategy gave a mean of 37.4 (median 26)
  against a predicted 37.7.

## Variant: choose direction too

As well as (or instead of) swapping the dice, you may reverse the direction of either
axis, e.g. move left instead of right, or down instead of up. Moves still wrap.

Expected turns under optimal play, for each combination of choices:

| Choices allowed | Without swapping dice | With swapping dice |
|---|---|---|
| No direction choice | 100.8 | 37.7 |
| Reverse horizontal | 45.6 | 18.7 |
| Reverse vertical | 43.9 | 17.7 |
| Reverse both | 21.7 | 10.8 |

With only forward moves, each die reaches 6 of the 10 positions along its axis.
Allowing reverse moves reaches all 9 other positions, so with both axes reversible you
can hit 100 in one throw from any square not in its row or column, given the right roll.

Check: 10,000 simulated games with every choice allowed gave a mean of 10.80 turns
(median 8) against a predicted 10.82.
