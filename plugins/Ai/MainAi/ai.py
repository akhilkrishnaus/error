from pyrogram import Client, filters
import requests 

@Client.on_message(filters.command(["ai"]))
async def modelai_command(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a query in /ai hi")
        return

    query = " ".join(message.command[1:])

    api = "https://horrid-api.vercel.app/mango"
    role = """Your name is Mr tom. Your owner is Albert Einstein @aktelegram1. 
              For Telegram, contact him at @aktelegram1. Owned by @aktelegram1. 
              Albert Einstein's GitHub: https://github.com/mallu-movie-world-dev1"""

    payload = {
        'messages': [
            {
                "role": "system",
                "content": role
            },
            {
                "role": "user", 
                "content": query
            }
        ],
        "model": "gpt-3.5-turbo"
    }

    response = requests.post(api, json=payload)
    response_json = response.json()

    response_text = "ʜᴇʏ: " + message.from_user.mention + "\n\nϙᴜᴇʀʏ: " + query + "\n\nʀᴇsᴜʟᴛ:\n" + response_json.get("response", "No response from the AI")

    await message.reply_text(response_text)
