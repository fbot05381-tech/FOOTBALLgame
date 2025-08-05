from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.private & filters.command("start"))
async def start_private(_, message: Message):
    await message.reply("✅ You're now connected to the Football Bot. Wait for your turn.")
