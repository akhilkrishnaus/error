from requests import get
from pyrogram import filters
from pyrogram.types import InputMediaPhoto
from pyrogram import Client

# Define the command
@Client.on_message(filters.command("wallpapers"))
async def pinterest(client, message):
    chat_id = message.chat.id
    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply("Input image name for search 🔍")

    msg = await message.reply("🔍")

    try:
        images = get(f"https://hoshi-api-f62i.onrender.com/api/wallpaper?query={query}").json()
        media_group = [InputMediaPhoto(media=url) for url in images["images"][:8]]

        await msg.edit(f"=> ✅ Fetched {len(media_group)} wallpapers...")
        
        await client.send_media_group(
            chat_id=chat_id, 
            media=media_group,
            reply_to_message_id=message.id)
        
        await msg.delete()
    except Exception as e:
        await msg.delete()
        await message.reply(f"Error\n{e}")

# Make sure to register the plugin
def register(app):
    app.add_handler(Client.on_message(filters.command("wallpapers"))(pinterest))
