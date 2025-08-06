from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "football_bot2",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
)

# ✅ Move handler imports AFTER bot definition
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

if __name__ == "__main__":
    print("⚽ Football Bot is running...")
    bot.run()
