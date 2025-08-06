from pyrogram import filters
from pyrogram.types import Message
from utils.states import games
from main import bot  # ✅ Import bot instead of using Client

print("✅ [score_afk.py] Score handler loaded")  # Debug

@bot.on_message(filters.command("score") & filters.group)
async def show_score(_, message: Message):
    chat_id = message.chat.id

    if chat_id not in games:
        return await message.reply("❌ No ongoing game.")

    score = games[chat_id].get("score", {"A": 0, "B": 0})
    await message.reply(
        f"🏆 Current Score:\n"
        f"Team A: {score['A']}\n"
        f"Team B: {score['B']}"
    )
