from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from utils.helpers import referee_image, organiser_image
from utils.buttons import referee_button, organiser_button

@Client.on_callback_query(filters.regex("^(team_mode|tournament_mode)$"))
async def mode_select_handler(_, cq: CallbackQuery):
    """
    Handles the game mode selection from the main menu (/start_football).
    Offers buttons to become Referee or Organiser.
    """
    mode = cq.data
    await cq.message.delete()

    if mode == "team_mode":
        await cq.message.chat.send_photo(
            photo=referee_image(),
            caption="🎮 *Team Mode Selected!*\nClick below if you're ready to become the referee.",
            reply_markup=InlineKeyboardMarkup([[referee_button()]])
        )

    elif mode == "tournament_mode":
        await cq.message.chat.send_photo(
            photo=organiser_image(),
            caption="🏆 *Tournament Mode Selected!*\nClick below if you're the organiser.",
            reply_markup=InlineKeyboardMarkup([[organiser_button()]])
        )
