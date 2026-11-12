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
