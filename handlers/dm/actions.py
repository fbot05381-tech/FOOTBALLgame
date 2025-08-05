from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.states import games

@Client.on_message(filters.command("trigger_dm") & filters.group)
async def send_action_buttons(_, message: Message):
    # TEMPORARY: Referee triggers it for testing
    chat_id = message.chat.id
    user = message.reply_to_message.from_user if message.reply_to_message else None

    if not user:
        return await message.reply("Reply to a player to trigger DM.")

    try:
        await _.send_message(
            user.id,
            "⚽️ Your move!\nChoose your action:",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("KICK", callback_data=f"k_{chat_id}"),
                    InlineKeyboardButton("PASS", callback_data=f"p_{chat_id}"),
                    InlineKeyboardButton("DEFENSIVE", callback_data=f"d_{chat_id}")
                ]]
            )
        )
        await message.reply(f"✅ Buttons sent to {user.first_name}.")
    except:
        await message.reply("❌ Player has not started the bot. Ask them to use /start in DM.")
