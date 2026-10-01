from bot.game import BOT, PLAYER, Game, best_bot_move


def test_player_can_make_move():
    game = Game()
    assert game.make_move(0, PLAYER)
    assert game.board[0] == PLAYER


def test_occupied_cell_is_rejected():
    game = Game()
    game.make_move(0, PLAYER)
    assert not game.make_move(0, BOT)


def test_winner_is_detected():
    game = Game()
    for position in (0, 1, 2):
        game.make_move(position, PLAYER)
    assert game.winner() == PLAYER
    assert game.is_over()


def test_draw_is_detected():
    game = Game()
    for position, mark in enumerate((PLAYER, BOT, PLAYER, PLAYER, BOT, BOT, BOT, PLAYER, PLAYER)):
        game.make_move(position, mark)
    assert game.is_draw()
    assert game.is_over()


def test_bot_takes_winning_move():
    game = Game()
    game.board = [BOT, BOT, " ", PLAYER, PLAYER, " ", " ", " ", " "]
    assert best_bot_move(game) == 2
