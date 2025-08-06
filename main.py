5import logging
from pyrogram import Client, filters
from config import API_ID, API_HASH, BOT_TOKEN
import asyncio

# ✅ Enable logging to debug startup
logging.basicConfig(level=logging.INFO)

# ✅ Fresh session name to avoid sqlite lock
bot = Client(
    "football_bot_fresh",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ Load handlers AFTER bot definition
import handlers.start
import handlers.mode_select
import handlers.referee_handler
import handlers.team_join
import handlers.team_balance
import handlers.captain_goalkeeper
import handlers.gameplay
import handlers.tournament_handler
import handlers.score_afk
import handlers.dm.start
import handlers.dm.actions
import handlers.dm.callbacks

# ✅ Test command
@bot.on_message(filters.command("ping"))
async def ping(_, message):
    await message.reply("🏓 Pong!")

# ✅ Notify owner in DM
async def notify_owner():
    try:
        await bot.send_message("me", "✅ Football Bot started successfully!")
    except Exception as e:
        print("❌ Could not send DM:", e)

# ✅ Proper way to start and notify
async def main():
    await bot.start()
    print("⚽ Football Bot is running...")
    await notify_owner()
    await bot.idle()  # Keeps the bot alive

if __name__ == "__main__":
    asyncio.run(main())
