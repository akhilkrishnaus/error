import asyncio
from pyrogram import Client, filters
import requests
from datetime import datetime

@Client.on_message(filters.command("bard"))
async def lexica_askbot(client, message):
    query = message.text.split()[1:]  # Split the message to get the query
    query = " ".join(query)  # Join the query parts
    
    if not query:
        await message.reply_text("Give An Input!!!")  # Prompt for input if query is empty
        return
    
    # Send a sticker in response to the command
    sticker = await message.reply_sticker("CAACAgQAAxkBAAEMiPtmoPu90QZmca02BV_0V_gaK4HWHQACbg8AAuHqsVDaMQeY6CcRojUE")
    
    await asyncio.sleep(1)  # Optional delay before deleting the sticker
    await sticker.delete()  # Delete the sticker after a short delay
    
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
            response = requests.post(api, json=payload)  # Send the request to the API
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()  # Parse the JSON response
            response_content = data.get('response', 'No response content')
        except requests.RequestException as e:
            response_content = f"Error: {e}"  # Handle request errors
        except ValueError:
            response_content = "Failed to parse response"  # Handle JSON parsing errors
        
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current date and time
        formatted_response = (
            f"ʜᴇʏ: {message.from_user.mention}\n\n"
            f"ϙᴜᴇʀʏ: {query}\n\n"
            f"ʀᴇsᴜʟᴛ:\n\n{response_content}\n\n"
            f"Date and Time (IST): {current_datetime}\n\n"
            f"ᴘʀᴏᴠɪᴅᴇᴅ ʙʏ <b><a href=https://t.me/mallumovieworldmain1>ᴍᴍᴡ ʙᴏᴛᴢ</a></b>\n\n"
            f"❣️𝚃𝙷𝙰𝙽𝙺𝚂 𝙵𝙾𝚁 𝚄𝚂𝙸𝙽𝙶 𝙼𝚈 𝚃𝙷𝙸𝚂 𝙵𝙴𝙰𝚃𝚄𝚁𝙴 😍"
        )

        await message.reply_text(formatted_response)  # Send the formatted response back to the user
    
    asyncio.create_task(get_response())  # Start the response fetching task
