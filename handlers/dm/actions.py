from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from utils.states import games
from main import bot  # ✅ Import the shared bot instance

print("✅ [dm/actions.py] DM action sender loaded")  # Debug

@bot.on_message(filters.command("trigger_dm") & filters.group)
async def send_action_buttons(_, message: Message):
    chat_id = message.chat.id
    user = message.reply_to_message.from_user if message.reply_to_message else None

    if not user:
        return await message.reply("👆 Reply to a player to trigger DM.")

    try:
        await bot.send_message(  # ✅ use `bot.send_message` directly
            user.id,
            "⚽️ Your move!\nChoose your action:",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("KICK", callback_data=f"k_{chat_id}"),
                    InlineKeyboardButton("PASS", callback_data=f"p_{chat_id}"),
                    InlineKeyboardButton("DEFENSIVE", callback_data=f"d_{chat_id}")
                ]
            ])
        )
        await message.reply(f"✅ Buttons sent to {user.first_name}.")
    except:
        await message.reply("❌ Player has not started the bot. Ask them to use /start in DM.")
