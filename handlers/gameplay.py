from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from utils.states import games, user_game
from asyncio import sleep
import random
from main import bot  # ✅ Import your bot

print("✅ [gameplay.py] Match gameplay handler loaded")  # Debug log

# Action buttons shown in user DM
action_buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("⚽ KICK", callback_data="act_kick")],
    [InlineKeyboardButton("📤 PASS", callback_data="act_pass")],
    [InlineKeyboardButton("🛡 DEFENSIVE", callback_data="act_defend")]
])

@bot.on_message(filters.command("start_match") & filters.group)
async def start_match(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    print(f"📥 [gameplay.py] /start_match by {user_id} in chat {chat_id}")  # Debug

    if chat_id not in games:
        return await message.reply("❌ No active game.")
    if games[chat_id]["referee"] != user_id:
        return await message.reply("❌ Only the referee can start the match.")

    await message.reply("🎮 Match started with 3 rounds of 15 minutes each (simulated).")

    for round_no in range(1, 4):
        games[chat_id]["round"] = round_no
        await bot.send_message(chat_id, f"🏁 Round {round_no} begins!")
        await start_round(chat_id)

    await bot.send_message(
        chat_id,
        "🏁 Match ended!\nFinal Score:\n"
        f"Team A: {games[chat_id]['score']['A']}\n"
        f"Team B: {games[chat_id]['score']['B']}"
    )

async def start_round(chat_id):
    all_players = games[chat_id]["teamA"] + games[chat_id]["teamB"]
    random.shuffle(all_players)

    for player_id in all_players:
        games[chat_id]["current_player"] = player_id
        games[chat_id]["ball_holder"] = player_id
        user_game[player_id] = chat_id

        try:
            await bot.send_message(
                player_id,
                "🎯 Your turn! Choose your action:",
                reply_markup=action_buttons
            )
        except Exception:
            await bot.send_message(
                chat_id,
                f"⚠️ Player [{player_id}](tg://user?id={player_id})'s DM is blocked."
            )

        await sleep(20)  # Wait 20 seconds for action

        if games[chat_id].get("current_player") == player_id:
            # Player didn’t act in time (AFK)
            games[chat_id]["yellow_cards"][player_id] = games[chat_id]["yellow_cards"].get(player_id, 0) + 1
            if games[chat_id]["yellow_cards"][player_id] >= 2:
                games[chat_id]["red_cards"].append(player_id)
                await bot.send_message(
                    chat_id,
                    f"🔴 Player [{player_id}](tg://user?id={player_id}) got RED card for being AFK."
                )
            else:
                await bot.send_message(
                    chat_id,
                    f"🟡 Player [{player_id}](tg://user?id={player_id}) is AFK. Yellow card given."
                )

        games[chat_id]["current_player"] = None

@bot.on_callback_query(filters.regex("^act_"))
async def action_choice(_, cq: CallbackQuery):
    user_id = cq.from_user.id
    chat_id = user_game.get(user_id)

    print(f"🎮 [gameplay.py] Action selected by {user_id} ({cq.data})")  # Debug

    if not chat_id or chat_id not in games:
        return await cq.answer("❌ No active game.")

    if games[chat_id]["current_player"] != user_id:
        return await cq.answer("⚠️ It's not your turn.", show_alert=True)

    action = cq.data.split("_")[1]
    team = "A" if user_id in games[chat_id]["teamA"] else "B"

    if action == "kick":
        scored = random.choice([True, False])
        if scored:
            games[chat_id]["score"][team] += 1
            await bot.send_message(chat_id, f"⚽ GOAL by [{user_id}](tg://user?id={user_id})! Team {team} scores!")
        else:
            await bot.send_message(chat_id, f"🥅 Missed shot by [{user_id}](tg://user?id={user_id}). No goal.")

    elif action == "pass":
        await bot.send_message(chat_id, f"📤 [{user_id}](tg://user?id={user_id}) passed the ball successfully.")

    elif action == "defend":
        await bot.send_message(chat_id, f"🛡 [{user_id}](tg://user?id={user_id}) chose to play defensive.")

    games[chat_id]["current_player"] = None
    await cq.answer("✅ Action received.")
    await cq.message.delete()
