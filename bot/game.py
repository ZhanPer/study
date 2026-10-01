from dataclasses import dataclass, field

EMPTY = " "
PLAYER = "X"
BOT = "O"
WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


@dataclass
class Game:
    board: list[str] = field(default_factory=lambda: [EMPTY] * 9)
    finished: bool = False

    def make_move(self, position: int, mark: str) -> bool:
        if self.finished or not 0 <= position < 9 or self.board[position] != EMPTY:
            return False
        self.board[position] = mark
        return True

    def winner(self) -> str | None:
        for a, b, c in WIN_LINES:
            if self.board[a] != EMPTY and self.board[a] == self.board[b] == self.board[c]:
                return self.board[a]
        return None

    def is_draw(self) -> bool:
        return self.winner() is None and EMPTY not in self.board

    def is_over(self) -> bool:
        return self.winner() is not None or self.is_draw()


def best_bot_move(game: Game) -> int:
    best_score = -float("inf")
    move = -1
    for i, cell in enumerate(game.board):
        if cell != EMPTY:
            continue
        game.board[i] = BOT
        score = _minimax(game.board, False)
        game.board[i] = EMPTY
        if score > best_score:
            best_score, move = score, i
    return move


def _minimax(board: list[str], maximizing: bool) -> int:
    result = _result(board)
    if result == BOT:
        return 1
    if result == PLAYER:
        return -1
    if EMPTY not in board:
        return 0

    scores = []
    for i, cell in enumerate(board):
        if cell == EMPTY:
            board[i] = BOT if maximizing else PLAYER
            scores.append(_minimax(board, not maximizing))
            board[i] = EMPTY
    return max(scores) if maximizing else min(scores)


def _result(board: list[str]) -> str | None:
    for a, b, c in WIN_LINES:
        if board[a] != EMPTY and board[a] == board[b] == board[c]:
            return board[a]
    return None
