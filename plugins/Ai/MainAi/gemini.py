import asyncio
from pyrogram import Client, filters
import requests
from datetime import datetime

@Client.on_message(filters.command("gemini"))
async def lexica_askbot(client, message):
    query = message.text.split()[1:]
    query = " ".join(query)
    
    if not query:
        await message.reply_text("Give An Input!!!")
        return
    
    sticker = await message.reply_sticker("CAACAgQAAxkBAAEMiPtmoPu90QZmca02BV_0V_gaK4HWHQACbg8AAuHqsVDaMQeY6CcRojUE")
    
    await asyncio.sleep(1)
    await sticker.delete()
    
    payload = {
        'messages': [
            {
                'role': "system",
                'content': "Your name is Mr. Tom, a language model created by Albert. His Telegram username is @aktelegram1. You can check out his GitHub profile at https://github.com/mallu-movie-world-dev1.",
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
            response_content = data.get('response', 'No response content')
        except requests.RequestException as e:
            response_content = f"Error: {e}"
        except ValueError:
            response_content = "Failed to parse response"
        
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_response = (
            f"ʜᴇʏ: {message.from_user.mention}\n\n"
            f"ϙᴜᴇʀʏ: {query}\n\n"
            f"ʀᴇsᴜʟᴛ:\n\n{response_content}\n\n"
            f"Date and Time (IST): {current_datetime}\n\n"
            f"ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ <b><a href=https://t.me/mallumovieworldmain1>ᴍᴍᴡ ʙᴏᴛᴢ</a></b>\n\n"
            f"❣️𝚃𝙷𝙰𝙽𝙺𝚂 𝙵𝙾𝚁 𝚄𝚂𝙸𝙽𝙶 𝙼𝚈 𝚃𝙷𝙸𝚂 𝙵𝙴𝙰𝚃𝚄𝚁𝙴 😍"
        )

        await message.reply_text(formatted_response)
    
    asyncio.create_task(get_response())
