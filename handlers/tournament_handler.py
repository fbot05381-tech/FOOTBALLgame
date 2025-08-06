from pyrogram import filters
from pyrogram.types import Message
from utils.states import game_states
from main import bot  # ✅ Import bot from main.py

print("✅ [tournament_handler.py] Tournament handler loaded")  # Debug

@bot.on_message(filters.command("create_tournament") & filters.group)
async def create_tournament(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    print(f"📥 [tournament_handler.py] /create_tournament from {user_id} in chat {chat_id}")  # Debug

    if chat_id not in game_states or game_states[chat_id].get("mode") != "tournament":
        return await message.reply("❌ Tournament mode not selected.")

    if user_id != game_states[chat_id].get("organizer"):
        return await message.reply("⚠️ Only the organizer can set up the tournament.")

    game_states[chat_id]["tournament"] = {
        "total_teams": 8,         # Can be made configurable later
        "players_per_team": 8,    # Same
        "teams": {f"Team{i+1}": [] for i in range(8)}
    }

    await message.reply(
        "✅ Tournament created with 8 teams and 8 players each.\n"
        "Players can now join using /join_teamX (replace X with 1-8)."
    )
