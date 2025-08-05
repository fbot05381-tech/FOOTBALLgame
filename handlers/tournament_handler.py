from pyrogram import Client, filters
from pyrogram.types import Message
from utils.states import game_states

@Client.on_message(filters.command("create_tournament") & filters.group)
async def create_tournament(client, message: Message):
    chat_id = message.chat.id

    if chat_id not in game_states or game_states[chat_id].get("mode") != "tournament":
        return await message.reply("❌ Tournament mode not selected.")

    user_id = message.from_user.id
    if user_id != game_states[chat_id].get("organizer"):
        return await message.reply("⚠️ Only the organizer can set up the tournament.")

    game_states[chat_id]["tournament"].update({
        "total_teams": 8,         # You can make this configurable later
        "players_per_team": 8,    # Same here
        "teams": {f"Team{i+1}": [] for i in range(8)}
    })

    await message.reply("✅ Tournament created with 8 teams and 8 players each.\nUse /join_teamX to join (replace X with 1-8).")
