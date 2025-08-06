from pyrogram import filters
from pyrogram.types import CallbackQuery
from utils.states import games
from main import bot  # ✅ Import shared bot instance

print("✅ [dm/callbacks.py] Action callback handler loaded")  # Debug

@bot.on_callback_query(filters.regex("^(k|p|d)_"))
async def handle_action_button(_, query: CallbackQuery):
    action, chat_id = query.data.split("_")
    user_id = query.from_user.id

    chat_id = int(chat_id)

    await query.message.delete()  # Remove old buttons

    action_map = {
        "k": "KICK ⚽",
        "p": "PASS 🏃",
        "d": "DEFENSIVE 🛡️"
    }

    # Save player move into game state (optional)
    games[chat_id]["last_action"] = {
        "user_id": user_id,
        "action": action_map[action]
    }

    await bot.send_message(user_id, f"✅ You chose: {action_map[action]}")
