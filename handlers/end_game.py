from pyrogram import Client, filters
from pyrogram.types import Message
from utils.states import games, user_game

@Client.on_message(filters.command("end_match") & filters.group)
async def end_match(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in games:
        return await message.reply("❌ No ongoing game.")

    if games[chat_id]["referee"] != user_id:
        return await message.reply("❌ Only the referee can end the match.")

    # Clean up
    all_players = games[chat_id]["teamA"] + games[chat_id]["teamB"]
    for uid in all_players:
        if user_game.get(uid) == chat_id:
            del user_game[uid]

    del games[chat_id]

    await message.reply("🛑 Match has been ended and data cleared.")

@Client.on_message(filters.command("status") & filters.group)
async def game_status(_, message: Message):
    chat_id = message.chat.id
    if chat_id not in games:
        return await message.reply("ℹ️ No active game in this group.")
    
    a = len(games[chat_id]["teamA"])
    b = len(games[chat_id]["teamB"])
    await message.reply(f"👥 Players:\nTeam A: {a} players\nTeam B: {b} players")

# Restriction middleware (optional safety)
@Client.on_message(filters.command(["start_football", "join_team", "start_match"]))
async def prevent_duplicates(_, message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    # Only one game per user at a time
    if user_id in user_game:
        if user_game[user_id] != chat_id:
            return await message.reply("⚠️ You're already in another game.")

    # One game per group
    if message.text.startswith("/start_football"):
        if chat_id in games:
            return await message.reply("⚠️ A game is already running in this group.")
