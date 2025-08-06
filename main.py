from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

# ✅ Pyrogram Client Initialization
bot = Client(
    "football_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# ✅ Manual Handler Imports (force-loads them)
import handlers.start
import handlers.mode_select
import handlers.referee_handler
import handlers.team_join
import handlers.team_balance
import handlers.captain_goalkeeper
import handlers.gameplay
import handlers.tournament_handler
import handlers.score_afk

# ✅ DM Handlers (optional)
import handlers.dm.start
import handlers.dm.actions
import handlers.dm.callbacks
import handlers.dm.position_check

if __name__ == "__main__":
    print("⚽ Football Bot is running...")
    bot.run()
