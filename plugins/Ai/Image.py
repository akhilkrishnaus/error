from HorridAPI import Async
from pyrogram import filters, Client 
from pyrogram.types import InputMediaPhoto

@Client.on_message(filters.command(["img", "image", "imagesearch"]))
async def images(bot, message):
    if len(message.command) < 2:
        return await message.reply_text("**Where is the query? 🤔\n\nPlease provide a query like:**\n\n`/img Luffy`")
    
    query = " ".join(message.command[1:])
    k = await message.reply_text("**Searching.. 🔍**")
    
    image = await Async().images(
        base_url="https://horrid-api.vercel.app/",
        query=query,
        page=7
    )
    
    MEDIA = []
    p = 0 
    for img in image["result"]:
        p += 1
        await k.edit(f"**⚡ Successfully fetched {p}**")
        MEDIA.append(InputMediaPhoto(media=img["images"]))
    
    if MEDIA:
        await message.reply_media_group(MEDIA)
        await k.delete()
    else:
        await k.edit("**No images found. 🙃**")
