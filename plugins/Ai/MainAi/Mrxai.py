import asyncio
from pyrogram import Client, filters
import requests
from datetime import datetime

@Client.on_message(filters.command("mrx"))
async def lexica_askbot(client, message):
    query = message.text.split()[1:]
    query = " ".join(query)
    
    if not query:
        await message.reply_text("Give An Input !!")
        return
    
    sticker = await message.reply_sticker("CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ")
    
    await asyncio.sleep(2)  # Adjust the delay as needed
    
    await sticker.delete()
    
    payload = {
        'messages': [
            {
                'role': "system",
                'content': "Your name is Mr.Tom, You are an AI developed by @MRXSUPPORTS and your owner is @aktelegram1.",
            },
            {
                'role': "user",
                'content': query,
            },
        ],
        "model_id": 23
    }

    api = 'https://api.qewertyy.dev/models'

    async def get_response():
        try:
            response = requests.post(api, json=payload)
            response.raise_for_status()  # Raises an error for bad status codes
            data = response.json()
            result = data.get('content', 'No response content')
        except requests.RequestException as e:
            result = f"Error: {e}"
        except ValueError:
            result = "Failed to parse response"
        
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_response = (
            f"ʜᴇʏ: {message.from_user.mention}\n\n"
            f"ϙᴜᴇʀʏ: {query}\n\n"
            f"ʀᴇsᴜʟᴛ:\n\n{result}\n\n"
            f"Date and Time (IST): {current_datetime}"
        )

        await message.reply_text(formatted_response)
    
    asyncio.create_task(get_response())
