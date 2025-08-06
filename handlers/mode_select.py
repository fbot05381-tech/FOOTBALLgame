from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from utils.helpers import referee_image, organiser_image
from utils.buttons import referee_button, organiser_button
from utils.states import game_states  # 🧠 Needed to store mode
from main import bot

print("✅ [mode_select.py] callback handler loaded")  # Debug

@bot.on_callback_query(filters.regex("^(team_mode|tournament_mode)$"))
async def mode_select_handler(_, cq: CallbackQuery):
    """
    Handles game mode selection after /start_football.
    Offers role-specific button: Referee or Organiser.
    """
    chat_id = cq.message.chat.id
    user_id = cq.from_user.id
    mode_selected = cq.data

    print(f"📥 [mode_select.py] Callback received: {mode_selected} from {user_id}")  # Debug

    await cq.message.delete()

    # 🧠 Safety: Ensure /start_football was used
    if chat_id not in game_states:
        return await cq.answer("❌ Please use /start_football first.", show_alert=True)

    # 🧠 Save mode
    game_states[chat_id]["mode"] = "team" if mode_selected == "team_mode" else "tournament"

    if mode_selected == "team_mode":
        await cq.message.chat.send_photo(
            photo=referee_image(),
            caption="🎮 *Team Mode Selected!*\nClick below if you're ready to become the referee.",
            reply_markup=InlineKeyboardMarkup([[referee_button()]])
        )

    elif mode_selected == "tournament_mode":
        await cq.message.chat.send_photo(
            photo=organiser_image(),
            caption="🏆 *Tournament Mode Selected!*\nClick below if you're the organiser.",
            reply_markup=InlineKeyboardMarkup([[organiser_button()]])
        )
