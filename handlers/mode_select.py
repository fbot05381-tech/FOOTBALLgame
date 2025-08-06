from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from utils.helpers import referee_image, organiser_image
from utils.buttons import referee_button, organiser_button
from main import bot  # ✅ Import the bot instance

print("✅ [mode_select.py] callback handler loaded")  # Debug

@bot.on_callback_query(filters.regex("^(team_mode|tournament_mode)$"))
async def mode_select_handler(_, cq: CallbackQuery):
    """
    Handles the game mode selection from the main menu (/start_football).
    Offers buttons to become Referee or Organiser.
    """
    print(f"📥 [mode_select.py] Callback received: {cq.data}")  # Debug

    await cq.message.delete()

    if cq.data == "team_mode":
        await cq.message.chat.send_photo(
            photo=referee_image(),
            caption="🎮 *Team Mode Selected!*\nClick below if you're ready to become the referee.",
            reply_markup=InlineKeyboardMarkup([[referee_button()]])
        )

    elif cq.data == "tournament_mode":
        await cq.message.chat.send_photo(
            photo=organiser_image(),
            caption="🏆 *Tournament Mode Selected!*\nClick below if you're the organiser.",
            reply_markup=InlineKeyboardMarkup([[organiser_button()]])
        )
