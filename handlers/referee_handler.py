from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, Message
from utils.states import games, user_game
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_callback_query(filters.regex("^become_referee$"))
async def handle_referee(_, cq: CallbackQuery):
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id

    if chat_id in games:
        return await cq.answer("⚠️ Game already running in this group.", show_alert=True)

    if user_id in user_game:
        return await cq.answer("❌ You are already in a game.", show_alert=True)

    # Create new game
    games[chat_id] = {
        "referee": user_id,
        "status": "waiting",
        "teamA": [],
        "teamB": [],
        "captains": {},
        "goalkeepers": {},
        "round": 0,
        "score": {"A": 0, "B": 0},
        "current_player": None,
        "ball_holder": None,
        "positions": {},
        "yellow_cards": {},
        "red_cards": [],
        "paused": False,
    }

    user_game[user_id] = chat_id

    await cq.answer("✅ You're now the referee.")
    await cq.message.edit_caption(
        caption=f"👨‍⚖️ Referee: {cq.from_user.mention}\n\nSend `/create_team` to start team setup.\nThis will be a 3 round game of 15 mins each!",
    )

@Client.on_message(filters.command("create_team") & filters.group)
async def create_team(_, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    if chat_id not in games or games[chat_id]["referee"] != user_id:
        return await message.reply("❌ Only the assigned referee can use this.")

    await message.reply(
        "**🛠 Team Creation Started!**\nPlayers can now join **Team A** using `/join_teamA`\n⏳ 2 minutes to join...",
    )

    # Start 2-min join for Team A
    await start_team_join_phase(_, chat_id, "A")

async def start_team_join_phase(client, chat_id, team):
    from utils.states import games
    from asyncio import sleep

    if team == "A":
        games[chat_id]["teamA"] = []
    else:
        games[chat_id]["teamB"] = []

    await sleep(120)

    team_name = "Team A" if team == "A" else "Team B"
    await client.send_message(chat_id, f"⛔ {team_name} joining closed.")

    # Next phase
    if team == "A":
        await client.send_message(chat_id, "📢 Now joining **Team B** with `/join_teamB`\n⏳ 2 minutes to join...")
        await start_team_join_phase(client, chat_id, "B")
    else:
        await client.send_message(chat_id, "✅ Both teams formed. Referee can now balance teams using `/add_teamA`, `/add_teamB`, or `/shift_member`.")
