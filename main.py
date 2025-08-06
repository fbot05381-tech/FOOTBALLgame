import logging
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# ✅ Enable logging to see what's going on
logging.basicConfig(level=logging.DEBUG)

# ✅ Define the bot with a fresh session name to avoid sqlite errors
bot = Client(
    "football_bot2",  # ← new session name
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ Import handlers AFTER bot is defined
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

# ✅ Add simple fallback test command
@bot.on_message(filters.command("ping"))
async def ping(_, message):
    await message.reply("🏓 Pong!")

# ✅ Optional: send DM to yourself to confirm start
async def notify_owner():
    try:
        await bot.send_message("me", "✅ Football Bot started successfully!")
    except Exception as e:
        print("❌ DM failed:", e)

if __name__ == "__main__":
    print("⚽ Football Bot is running...")

    # ✅ Start bot, then run DM function and loop
    bot.start()  # Start client manually
    import asyncio
    asyncio.get_event_loop().run_until_complete(notify_owner())  # Send DM
    bot.run()  # Run forever
