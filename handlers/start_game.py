from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.states import game_states

@Client.on_message(filters.command("start_football") & filters.group)
async def start_football(_, message: Message):
    if message.chat.id in game_states:
        return await message.reply("⚠️ A game is already running in this group.")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🏆 Team Mode", callback_data="team_mode")],
        [InlineKeyboardButton("🎯 Tournament Mode", callback_data="tournament_mode")]
    ])
    await message.reply_animation(
        animation="https://media.tenor.com/BhkWZ-DXQwEAAAAC/football-game.gif",
        caption="⚽ Welcome to Football Battle!\nChoose a mode to begin:",
        reply_markup=keyboard
    )

@Client.on_callback_query(filters.regex("team_mode"))
async def select_team_mode(client, callback):
    await callback.message.delete()
    game_states[callback.message.chat.id] = {
        "mode": "team",
        "referee": None,
        "teams": {"A": [], "B": []},
        "round": 0,
    }
    await callback.message.chat.send_animation(
        animation="https://media.tenor.com/iVScxMmUft4AAAAd/referee-football.gif",
        caption="🎮 Click below if you want to be the Referee!",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🧍 I'm the Referee", callback_data="referee_join")]
        ])
    )

@Client.on_callback_query(filters.regex("tournament_mode"))
async def select_tournament_mode(client, callback):
    await callback.message.delete()
    game_states[callback.message.chat.id] = {
        "mode": "tournament",
        "organizer": callback.from_user.id,
        "tournament": {
            "total_teams": 0,
            "players_per_team": 0,
            "teams": {},
            "current_game": None
        }
    }

    await callback.message.chat.send_message(
        f"🎯 <b>Tournament Mode</b> activated by {callback.from_user.mention}.\n"
        "Use /create_tournament to begin setup."
    )
