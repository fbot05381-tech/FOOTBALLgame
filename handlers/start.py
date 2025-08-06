from pyrogram.types import Message, InlineKeyboardMarkup
from pyrogram import filters
from utils.helpers import random_football_gif
from utils.buttons import team_mode_button, tournament_mode_button
from main import bot  # ✅ bot imported from main.py

print("✅ [start.py] /start_football handler loaded")  # Debug: handler load confirmation

@bot.on_message(filters.command("start_football") & filters.group)
async def start_football(_, message: Message):
    print(f"📥 [start.py] /start_football received from chat {message.chat.id}")  # Debug: command received

    await message.reply_animation(
        animation=random_football_gif(),
        caption="🏟 **Welcome to Telegram Football!**\nChoose your game mode:",
        reply_markup=InlineKeyboardMarkup([
            [team_mode_button()],
            [tournament_mode_button()]
        ])
    )
