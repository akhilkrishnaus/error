from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters, enums

@Client.on_message(filters.command('support'))
async def ai_generate_private(client, message):
    # Define the buttons in one row
    buttons = [[
        InlineKeyboardButton("Support", url="https://t.me/MRXSUPPORTS"),
        InlineKeyboardButton("Update", url="https://t.me/mallumovieworldmain1")  # Added a new button
    ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    # Use triple quotes for multi-line string
    await message.reply_text(
        text="""🧏 Click here to reach out to the official 
Support for @Kevinbotmallubot.

Thank you! ❤️""",
        reply_markup=reply_markup
    )
