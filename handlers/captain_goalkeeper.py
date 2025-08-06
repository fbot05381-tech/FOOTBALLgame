from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.states import games
from main import bot  # ✅ Import bot

print("✅ [captain_goalkeeper.py] Captain & Goalkeeper handler loaded")  # Debug

# 🎖️ REFEREE assigns captain via buttons
@bot.on_message(filters.command("choose_captain") & filters.group)
async def choose_captain(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    print(f"📥 [captain_goalkeeper.py] /choose_captain used in chat {chat_id}")  # Debug

    if chat_id not in games or games[chat_id]["referee"] != user_id:
        return await message.reply("❌ Only the referee can choose captains.")

    await message.reply(
        "👑 Click below to assign Team Captains:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Captain - Team A", callback_data="captain_A")],
            [InlineKeyboardButton("Captain - Team B", callback_data="captain_B")]
        ])
    )

# 👤 Player clicks to become Captain
@bot.on_callback_query(filters.regex(r"^captain_(A|B)$"))
async def set_captain(_, cq: CallbackQuery):
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id
    team = cq.data.split("_")[1]

    print(f"🎯 [captain_goalkeeper.py] captain_{team} selected by {user_id}")  # Debug

    if user_id not in games[chat_id][f"team{team}"]:
        return await cq.answer("❌ You must be in that team to become captain.", show_alert=True)

    if team in games[chat_id]["captains"]:
        return await cq.answer("⚠️ Captain already assigned.", show_alert=True)

    games[chat_id]["captains"][team] = user_id
    await cq.answer("✅ You are now the captain.")

    try:
        await cq.message.edit_caption(f"🎉 {cq.from_user.mention} is now the Captain of Team {team}")
    except:
        await cq.message.edit_text(f"🎉 {cq.from_user.mention} is now the Captain of Team {team}")

# 🧤 Referee assigns goalkeeper by index
@bot.on_message(filters.command("set_gk") & filters.group)
async def set_goalkeeper(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    parts = message.text.split()

    print(f"📥 [captain_goalkeeper.py] /set_gk received in chat {chat_id}")  # Debug

    if chat_id not in games or games[chat_id]["referee"] != user_id:
        return await message.reply("❌ Only the referee can set goalkeepers.")

    if len(parts) != 3:
        return await message.reply("Usage: /set_gk A 3")

    team, index = parts[1], parts[2]
    if team not in ["A", "B"]:
        return await message.reply("⚠️ Team must be A or B.")

    try:
        idx = int(index) - 1
    except ValueError:
        return await message.reply("⚠️ Invalid number.")

    player_list = games[chat_id][f"team{team}"]
    if idx < 0 or idx >= len(player_list):
        return await message.reply("❌ Invalid player index.")

    gk_id = player_list[idx]

    # Optional: Prevent captain from being GK
    if gk_id == games[chat_id]["captains"].get(team):
        return await message.reply("⚠️ Captain cannot be the goalkeeper.")

    games[chat_id]["goalkeepers"][team] = gk_id

    try:
        user = await bot.get_users(gk_id)
        mention = user.mention
    except:
        mention = f"`{gk_id}`"

    await message.reply(f"🧤 Goalkeeper of Team {team} is {mention}.")
