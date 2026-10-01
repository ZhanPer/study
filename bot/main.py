import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from dotenv import load_dotenv

from bot.game import BOT, PLAYER, Game, best_bot_move

load_dotenv()
logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")

bot = Bot(BOT_TOKEN)
dp = Dispatcher()
games: dict[int, Game] = {}


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎮 Начать игру", callback_data="new_game")]
    ])


def board_keyboard(game: Game) -> InlineKeyboardMarkup:
    rows = []
    for row in range(3):
        rows.append([
            InlineKeyboardButton(
                text=game.board[row * 3 + col] if game.board[row * 3 + col] != " " else "⬜",
                callback_data=f"move:{row * 3 + col}",
            )
            for col in range(3)
        ])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def result_text(game: Game) -> str:
    winner = game.winner()
    if winner == PLAYER:
        return "🏆 Ты победил!"
    if winner == BOT:
        return "🤖 Я победил!"
    return "🤝 Ничья!"


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Привет! 👋\nЯ умею играть в крестики-нолики.\n\nСыграем?",
        reply_markup=start_keyboard(),
    )


@dp.message(F.text)
async def hello(message: Message) -> None:
    await message.answer(
        "Привет! 👋 Давай сыграем в крестики-нолики?",
        reply_markup=start_keyboard(),
    )


@dp.callback_query(F.data == "new_game")
async def new_game(callback: CallbackQuery) -> None:
    game = Game()
    games[callback.from_user.id] = game
    await callback.message.edit_text(
        "Твоя очередь. Ты играешь ❌",
        reply_markup=board_keyboard(game),
    )
    await callback.answer()


@dp.callback_query(F.data.startswith("move:"))
async def move(callback: CallbackQuery) -> None:
    game = games.get(callback.from_user.id)
    if game is None:
        await callback.answer("Сначала начни новую игру.", show_alert=True)
        return

    position = int(callback.data.split(":")[1])
    if not game.make_move(position, PLAYER):
        await callback.answer("Эта клетка уже занята.", show_alert=True)
        return

    if game.is_over():
        game.finished = True
        await callback.message.edit_text(result_text(game), reply_markup=start_keyboard())
        await callback.answer()
        return

    bot_move = best_bot_move(game)
    game.make_move(bot_move, BOT)

    if game.is_over():
        game.finished = True
        await callback.message.edit_text(result_text(game), reply_markup=start_keyboard())
    else:
        await callback.message.edit_reply_markup(reply_markup=board_keyboard(game))
        await callback.answer("Теперь твой ход!")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
