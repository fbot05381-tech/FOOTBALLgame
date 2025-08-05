from pyrogram import Client, filters
from pyrogram.types import Message
from utils.states import games

@Client.on_message(filters.command("my_position") & filters.group)
async def show_position(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in games:
        return await message.reply("❌ No active match.")

    pos_data = games[chat_id].get("player_positions", {}).get(user_id)
    if not pos_data:
        return await message.reply("❌ You're not in any team.")

    x, y = pos_data["position"]
    await message.reply(f"📍 Your position: X = {x}, Y = {y}")
