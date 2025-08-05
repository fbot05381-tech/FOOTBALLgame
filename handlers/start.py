from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from utils.helpers import random_football_gif
from utils.buttons import team_mode_button, tournament_mode_button

@Client.on_message(filters.command("start_football") & filters.group)
async def start_football(_, message: Message):
    """
    This command starts the football game setup in a group.
    It shows a GIF and buttons to choose between Team Mode and Tournament Mode.
    """
    await message.reply_animation(
        animation=random_football_gif(),
        caption="🏟 **Welcome to Telegram Football!**\nChoose your game mode:",
        reply_markup=InlineKeyboardMarkup([
            [team_mode_button()],
            [tournament_mode_button()]
        ])
    )
