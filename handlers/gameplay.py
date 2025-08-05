from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.states import games, user_game
from asyncio import sleep
import random

action_buttons = InlineKeyboardMarkup([
    [InlineKeyboardButton("⚽ KICK", callback_data="act_kick")],
    [InlineKeyboardButton("📤 PASS", callback_data="act_pass")],
    [InlineKeyboardButton("🛡 DEFENSIVE", callback_data="act_defend")]
])

@Client.on_message(filters.command("start_match") & filters.group)
async def start_match(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in games:
        return await message.reply("❌ No active game.")
    if games[chat_id]["referee"] != user_id:
        return await message.reply("❌ Only the referee can start the match.")

    await message.reply("🎮 Match started with 3 rounds of 15 minutes each (simulated).")

    for round_no in range(1, 4):
        games[chat_id]["round"] = round_no
        await _.send_message(chat_id, f"🏁 Round {round_no} begins!")
        await start_round(_, chat_id)

    await _.send_message(chat_id, "🏁 Match ended!\nFinal Score:\n"
                                   f"Team A: {games[chat_id]['score']['A']}\n"
                                   f"Team B: {games[chat_id]['score']['B']}")

async def start_round(client, chat_id):
    all_players = games[chat_id]["teamA"] + games[chat_id]["teamB"]
    random.shuffle(all_players)

    for player_id in all_players:
        games[chat_id]["current_player"] = player_id
        games[chat_id]["ball_holder"] = player_id

        try:
            await client.send_message(
                player_id,
                "🎯 Your turn! Choose your action:",
                reply_markup=action_buttons
            )
        except:
            await client.send_message(chat_id, f"⚠️ Player [{player_id}](tg://user?id={player_id})'s DM is blocked.")

        await sleep(20)  # 20s timer
        if games[chat_id].get("current_player") == player_id:
            # Player didn’t act (AFK)
            games[chat_id]["yellow_cards"][player_id] = games[chat_id]["yellow_cards"].get(player_id, 0) + 1
            if games[chat_id]["yellow_cards"][player_id] >= 2:
                games[chat_id]["red_cards"].append(player_id)
                await client.send_message(chat_id, f"🔴 Player [{player_id}](tg://user?id={player_id}) got RED card for being AFK.")
            else:
                await client.send_message(chat_id, f"🟡 Player [{player_id}](tg://user?id={player_id}) is AFK. Yellow card given.")

        games[chat_id]["current_player"] = None

# Button response
@Client.on_callback_query(filters.regex("^act_"))
async def action_choice(_, cq):
    user_id = cq.from_user.id
    chat_id = user_game.get(user_id)
    if not chat_id or chat_id not in games:
        return await cq.answer("❌ No active game.")

    if games[chat_id]["current_player"] != user_id:
        return await cq.answer("⚠️ It's not your turn.", show_alert=True)

    action = cq.data.split("_")[1]

    if action == "kick":
        scored = random.choice([True, False])
        team = "A" if user_id in games[chat_id]["teamA"] else "B"
        if scored:
            games[chat_id]["score"][team] += 1
            await _.send_message(chat_id, f"⚽ GOAL by [{user_id}](tg://user?id={user_id})! Team {team} scores!")
        else:
            await _.send_message(chat_id, f"🥅 Missed shot by [{user_id}](tg://user?id={user_id}). No goal.")
    
    elif action == "pass":
        await _.send_message(chat_id, f"📤 [{user_id}](tg://user?id={user_id}) passed the ball successfully.")

    elif action == "defend":
        await _.send_message(chat_id, f"🛡 [{user_id}](tg://user?id={user_id}) chose to play defensive.")

    games[chat_id]["current_player"] = None
    await cq.answer("✅ Action received.")
    await cq.message.delete()
