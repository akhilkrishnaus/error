import requests
import io
from pyrogram import Client, filters

@Client.on_message(filters.command(["wiki", "wikipedia"]))
async def wikipedia(client, message):
    if len(message.text.split()) < 2:
        return await message.reply("Give An Input!!")
    msg = await message.reply("Searching🔎...")
    query = " ".join(message.command[1:])
    try:
        response = requests.get(f'https://horrid-api-yihb.onrender.com/wiki?query={query}')
        result = response.json()
        if 'error' in result:
            await msg.edit(result['error'])
        else:
            if len(result['result']) > 3700:
                k = result['result']
                with io.BytesIO(str.encode(k)) as output:
                    output.name = "wikipedia.txt"
                    await message.reply_document(document=output)
            else:
                await msg.edit(result['result'])
    except Exception as e:
        print(e)
