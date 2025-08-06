import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN

# ✅ Enable logging
logging.basicConfig(level=logging.INFO)

# ✅ New session name
bot = Client(
    "football_test_bot",  # change this to force fresh session
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ Simple working test command
@bot.on_message(filters.command("start"))
async def start_cmd(_, message: Message):
    await message.reply("✅ Football Bot is working!")

if __name__ == "__main__":
    print("⚽ Football Bot is running...")
    bot.run()
