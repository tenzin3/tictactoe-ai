"""Create the tic-tac-toe dataset: every position, with its best moves.

    python prepare.py

No download is needed: tic-tac-toe is small enough to list every position that
can occur in a real game and work out the perfect move in each one with the
minimax algorithm. The result is written to data/positions.csv.

Squares are numbered 0-8, left to right, top to bottom:

    0 | 1 | 2
    3 | 4 | 5
    6 | 7 | 8
"""
import csv
import os
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8),   # rows
         (0, 3, 6), (1, 4, 7), (2, 5, 8),   # columns
         (0, 4, 8), (2, 4, 6)]              # diagonals


def winner(board):
    """'X' or 'O' if that player has three in a row, otherwise None."""
    for a, b, c in LINES:
        if board[a] != "." and board[a] == board[b] == board[c]:
            return board[a]
    return None


def to_move(board):
    """X always starts, so it is X's turn whenever both have played equally often."""
    return "X" if board.count("X") == board.count("O") else "O"


def play(board, square):
    return board[:square] + to_move(board) + board[square + 1:]


@lru_cache(maxsize=None)
def score(board):
    """How the game ends with perfect play, from the side to move's point of view.

    Positive = the side to move wins, 0 = draw, negative = it loses. Faster wins
    score higher (10 minus the number of moves played), so the best move wins as
    quickly as possible and, when losing, holds out as long as possible.
    """
    if winner(board):                       # the previous player just won
        return -(10 - board.count("."))
    if "." not in board:
        return 0
    return max(-score(play(board, s)) for s in range(9) if board[s] == ".")


def all_positions():
    """Every position reachable from the empty board in which the game is not over."""
    seen, todo = set(), ["........."]
    while todo:
        board = todo.pop()
        if board in seen or winner(board) or "." not in board:
            continue
        seen.add(board)
        todo.extend(play(board, s) for s in range(9) if board[s] == ".")
    return sorted(seen, key=lambda b: (9 - b.count("."), b))


def main():
    rows = []
    for board in all_positions():
        empty = [s for s in range(9) if board[s] == "."]
        value = {s: -score(play(board, s)) for s in empty}
        best = max(value.values())
        rows.append({
            "board": board,
            "to_move": to_move(board),
            "moves_played": 9 - len(empty),
            "best_moves": " ".join(str(s) for s in empty if value[s] == best),
            "result": (best > 0) - (best < 0),     # 1 win, 0 draw, -1 loss with perfect play
        })

    os.makedirs("data", exist_ok=True)
    with open("data/positions.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    print("Wrote %d positions to data/positions.csv" % len(rows))
    print("  X to move: %d, O to move: %d" % (sum(r["to_move"] == "X" for r in rows),
                                               sum(r["to_move"] == "O" for r in rows)))
    for value, name in ((1, "win"), (0, "draw"), (-1, "loss")):
        print("  side to move can force a %-4s: %d" % (name, sum(r["result"] == value for r in rows)))
    print("  positions with more than one best move: %d" % sum(" " in r["best_moves"] for r in rows))


if __name__ == "__main__":
    main()
