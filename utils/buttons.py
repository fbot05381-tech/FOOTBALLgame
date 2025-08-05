from pyrogram.types import InlineKeyboardButton

def team_mode_button():
    return InlineKeyboardButton("⚽ Team Mode", callback_data="team_mode")

def tournament_mode_button():
    return InlineKeyboardButton("🏆 Tournament Mode", callback_data="tournament_mode")

def referee_button():
    return InlineKeyboardButton("🎩 I'm the Referee", callback_data="become_referee")

def organiser_button():
    return InlineKeyboardButton("📋 I'm the Organiser", callback_data="become_organiser")
