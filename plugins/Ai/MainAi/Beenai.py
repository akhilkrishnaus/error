import asyncio
from pyrogram import Client, filters
import requests
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.command(["been"]))
async def lexica_askbot(client, message):
    query = message.text.split()[1:]
    query = " ".join(query)
    
    if not query:
        await message.reply_text("Usage: /been who is your owner")
        return
    
    sticker = await message.reply_sticker("CAACAgQAAxkBAAEMiPtmoPu90QZmca02BV_0V_gaK4HWHQACbg8AAuHqsVDaMQeY6CcRojUE")
    
    await asyncio.sleep(1)
    await sticker.delete()
    
    payload = {
        'messages': [
            {
                'role': "system",
                'content': "You are a helpful assistant. Your name is Mr. Tom. Your owner is Albert @aktelegram1. You are a stern person. Your developer is Albert. For Telegram, contact him at @aktelegram1. Owned by @aktelegram1. Albert GitHub: https://github.com/mallu-movie-world-dev1 check it out ✅",
            },
            {
                'role': "user",
                'content': query,
            },
        ],
        "model": "gemma-7b-it"
    }

    api = 'https://horrid-api.vercel.app/mango'

    async def get_response():
        try:
            response = requests.post(api, json=payload)
            response.raise_for_status()
            data = response.json()
            response_text = data.get('response', 'No response content')
        except requests.RequestException as e:
            response_text = f"Error: {e}"
        except ValueError:
            response_text = "Failed to parse response"
        
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_response = (
            f"ʜᴇʏ: {message.from_user.mention}\n\n"
            f"ϙᴜᴇʀʏ: {query}\n\n"
            f"ʀᴇsᴜʟᴛ:\n\n{response_text}\n\n"
            f"Date and Time (IST): {current_datetime}\n\n"
            f"ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ <b><a href=https://t.me/mallumovieworldmain1>ᴍᴍᴡ ʙᴏᴛᴢ</a></b>\n\n"
            f"❣️𝚃𝙷𝙰𝙽𝙺𝚂 𝙵𝙾𝚁 𝚄𝚂𝙸𝙽𝙶 𝙼𝚈 𝚃𝙷𝙸𝚂 𝙵𝙴𝙰𝚃𝚄𝚁𝙴"
        )

        reply_markup = InlineKeyboardMarkup(
            [[InlineKeyboardButton("❌close here ❌", callback_data="close_response")]]
        )

        await message.reply_text(formatted_response, reply_markup=reply_markup)

    asyncio.create_task(get_response())

@Client.on_callback_query(filters.regex("close_response"))
async def close_response(client, callback_query):
    await callback_query.message.delete()
    await callback_query.answer()
