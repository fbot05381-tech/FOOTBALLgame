from pyrogram import Client, filters
from pyrogram.types import Message

# This module is reserved for:
# - AFK detection
# - Yellow/Red card logic
# - Score tracking

# You can implement timeouts and referee control here in future.

@Client.on_message(filters.command("score") & filters.group)
async def show_score(_, message: Message):
    chat_id = message.chat.id
    # Placeholder: replace with real score tracking from your `games` state
    await message.reply("🏆 Current score:\nTeam A: 0\nTeam B: 0")
