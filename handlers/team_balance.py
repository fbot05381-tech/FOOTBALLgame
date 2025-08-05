from pyrogram import Client, filters
from pyrogram.types import Message
from utils.states import games, user_game

@Client.on_message(filters.command(["add_teamA", "add_teamB"]) & filters.group)
async def add_to_team(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    command = message.command[0]
    
    if chat_id not in games or games[chat_id]["referee"] != user_id:
        return await message.reply("❌ Only the referee can use this.")

    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to the user you want to add.")

    target_user = message.reply_to_message.from_user
    target_id = target_user.id

    # Remove from previous team
    if target_id in games[chat_id]["teamA"]:
        games[chat_id]["teamA"].remove(target_id)
    if target_id in games[chat_id]["teamB"]:
        games[chat_id]["teamB"].remove(target_id)

    # Add to new team
    if "teamA" in command:
        games[chat_id]["teamA"].append(target_id)
        await message.reply(f"✅ {target_user.mention} added to Team A.")
    else:
        games[chat_id]["teamB"].append(target_id)
        await message.reply(f"✅ {target_user.mention} added to Team B.")

    user_game[target_id] = chat_id

@Client.on_message(filters.command("shift_member") & filters.group)
async def shift_member(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in games or games[chat_id]["referee"] != user_id:
        return await message.reply("❌ Only the referee can use this.")

    if not message.reply_to_message:
        return await message.reply("⚠️ Reply to the user you want to shift.")

    target_user = message.reply_to_message.from_user
    target_id = target_user.id

    if target_id in games[chat_id]["teamA"]:
        games[chat_id]["teamA"].remove(target_id)
        games[chat_id]["teamB"].append(target_id)
        await message.reply(f"🔁 Shifted {target_user.mention} to Team B.")
    elif target_id in games[chat_id]["teamB"]:
        games[chat_id]["teamB"].remove(target_id)
        games[chat_id]["teamA"].append(target_id)
        await message.reply(f"🔁 Shifted {target_user.mention} to Team A.")
    else:
        await message.reply("⚠️ This player is not in any team.")
