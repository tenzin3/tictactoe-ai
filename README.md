# tictactoe-ai

A machine-learning player for tic-tac-toe (noughts and crosses, XO). The
plan: prepare every position with its best move, train a network to predict
that move, then play against it. The game is small enough that every step runs
in seconds and the answers can be checked exactly.

## Data preparation

```bash
python prepare.py
```

No download and no extra packages are needed. The script lists every position
that can occur in a real game, works out the perfect move in each one with the
**minimax** algorithm, and writes `data/positions.csv`. It runs in under a
second.

Output:

```
Wrote 4520 positions to data/positions.csv
  X to move: 2423, O to move: 2097
  side to move can force a win : 2836
  side to move can force a draw: 1052
  side to move can force a loss: 632
  positions with more than one best move: 1514
```

### How it works

1. **List the positions.** Starting from the empty board, play every possible
   move, then every reply, and so on, keeping each position where the game is
   not yet over. There are exactly 4,520 of them.
2. **Score every move with minimax.** Minimax looks ahead to the end of the
   game, assuming both players always play their best: a player picks the move
   that is best for them, knowing the opponent will then pick the move that is
   best for the opponent. This gives the true outcome of every move: win, draw
   or loss.
3. **Prefer fast wins.** A win in fewer moves scores higher, and when losing, a
   move that holds out longer scores higher. Without this, the "best" move
   could be one that wins eventually while ignoring a win available right now.
4. **Record the best moves.** Often several moves are equally good, so all of
   them are kept.

## Data description

`data/positions.csv` has one row per position. This is the prepared data that
the model trains on; there is no raw data, because nothing is downloaded.

### Columns

| Column | Example | Meaning |
|---|---|---|
| `board` | `X...O....` | The 9 squares, read left to right, top to bottom: `X`, `O`, or `.` for empty |
| `to_move` | `X` | Whose turn it is. X always moves first |
| `moves_played` | `2` | How many moves have been made so far (0-8) |
| `best_moves` | `2 6` | Every square that is a perfect move here, separated by spaces |
| `result` | `0` | How the game ends if both players play perfectly from here, for the side to move: `1` win, `0` draw, `-1` loss |

### Reading the board

The squares are numbered 0 to 8:

```
0 | 1 | 2
--+---+--
3 | 4 | 5
--+---+--
6 | 7 | 8
```

So the board string `XX.OO....` means:

```
X | X | .
--+---+--
O | O | .
--+---+--
. | . | .
```

The dots are **empty squares**. Every board string is exactly 9 characters, so
the character at position 4 is always the centre square.

### Example rows

**The empty board**

```
board ......... , to_move X , best_moves 0 1 2 3 4 5 6 7 8 , result 0
```

Every first move is a perfect move, and with perfect play the game is always a
draw.

**X opened in a corner**

```
board X........ , to_move O , best_moves 4 , result 0

X | . | .
--+---+--
. | . | .
--+---+--
. | . | .
```

O's only perfect reply is the centre (square 4). Any other move lets X force a
win.

**Win now**

```
board XX.OO.... , to_move X , best_moves 2 , result 1

X | X | .        X plays square 2: three in a row
--+---+--
O | O | .
--+---+--
. | . | .
```

Square 5 would also stop O, but square 2 wins immediately, so it is the only
best move.

**Block**

```
board XX..O.... , to_move O , best_moves 2 , result 0

X | X | .        O must play square 2,
--+---+--        or X wins next move
. | O | .
--+---+--
. | . | .
```

### Facts about the data

- 4,520 positions: 2,423 with X to move and 2,097 with O to move.
- The side to move can force a win in 2,836, a draw in 1,052, and is lost
  whatever it does in 632 (those come from earlier mistakes by that player).
- 1,514 positions have more than one perfect move.
- These match the known facts of tic-tac-toe: 4,520 reachable unfinished
  positions, and a draw with perfect play from the start.
