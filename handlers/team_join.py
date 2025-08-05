from pyrogram import Client, filters
from pyrogram.types import Message
from utils.states import games, user_game

@Client.on_message(filters.command(["join_teamA", "join_teamB"]) & filters.group)
async def join_team(_, message: Message):
    user = message.from_user
    chat_id = message.chat.id
    user_id = user.id
    cmd = message.command[0]

    if chat_id not in games:
        return await message.reply("❌ No active game in this group.")

    if user_id in user_game:
        return await message.reply("⚠️ You're already in a game.")

    team = "A" if "A" in cmd else "B"
    team_list = games[chat_id]["teamA"] if team == "A" else games[chat_id]["teamB"]

    if len(team_list) >= 8:
        return await message.reply(f"⚠️ Team {team} is full (8 players).")

    team_list.append(user_id)
    user_game[user_id] = chat_id
    await message.reply(f"✅ {user.mention} joined **Team {team}**.")
