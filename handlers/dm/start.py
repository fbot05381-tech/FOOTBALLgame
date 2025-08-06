from pyrogram import filters
from pyrogram.types import Message
from main import bot  # ✅ Import the shared bot instance

print("✅ [dm/start.py] Loaded")

@bot.on_message(filters.private & filters.command("start"))
async def start_private(_, message: Message):
    await message.reply("✅ You're now connected to the Football Bot. Wait for your turn.")
