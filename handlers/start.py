from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup
from utils.helpers import random_football_gif
from utils.buttons import team_mode_button, tournament_mode_button
from utils.states import games, game_states  # 🧠 Add this
from main import bot

print("✅ [start.py] /start_football handler loaded")

@bot.on_message(filters.command("start_football") & filters.group)
async def start_football(_, message: Message):
    chat_id = message.chat.id
    user = message.from_user

    print(f"📥 [start.py] /start_football from chat {chat_id}")

    if chat_id in games:
        return await message.reply("⚠️ A game is already running in this group.")

    # 🧠 Initialize base game state
    games[chat_id] = {
        "teamA": [],
        "teamB": [],
        "referee": user.id,
        "captains": {"A": None, "B": None},
        "goalkeepers": {"A": None, "B": None},
        "yellow_cards": {},
        "red_cards": [],
        "score": {"A": 0, "B": 0},
        "round": 0,
        "ball_holder": None,
        "current_player": None
    }

    # 🧠 Store game mode state
    game_states[chat_id] = {
        "mode": None,
        "organizer": user.id,
    }

    await message.reply_animation(
        animation=random_football_gif(),
        caption="🏟 **Welcome to Telegram Football!**\nChoose your game mode:",
        reply_markup=InlineKeyboardMarkup([
            [team_mode_button()],
            [tournament_mode_button()]
        ])
    )

from pyrogram import filters
from pyrogram.types import Message
from main import bot  # ✅ Make sure bot is imported

@bot.on_message(filters.command("start"))
async def start_command(_, message: Message):
    await message.reply("👋 Hello! I'm your Football Bot.\nUse /start_football in a group to begin the game!")
