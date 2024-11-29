
from base64 import b64decode
from io import BytesIO
import aiohttp
from pyrogram import filters, Client
from pyrogram.types import Message

async def take_screenshot(url: str, full: bool = False):
    url = "https://" + url if not url.startswith("http") else url
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.qewertyy.dev/webss?url={url}") as response:
            image_data = await response.read()
    file = BytesIO(image_data)
    file.name = "webss.jpg"
    return file

async def eor(msg: Message, **kwargs):
    func = (
        (msg.edit_text if msg.from_user.is_self else msg.reply)
        if msg.from_user
        else msg.reply
    )
    return await func(**kwargs)

@Client.on_message(filters.command(["webss", "ss", "webshot"]))
async def take_ss(_, message: Message):
    if len(message.command) < 2:
        return await eor(message, text="Please provide a URL to fetch the web screenshot.")

    if len(message.command) == 2:
        url = message.text.split(None, 1)[1]
        full = True
    elif len(message.command) == 3:
        url = message.text.split(None, 2)[1]
        full = message.text.split(None, 2)[2].lower().strip() in [
            "yes",
            "y",
            "1",
            "true",
        ]
    else:
        return await eor(message, text="Invalid command.")

    m = await eor(message, text="Capturing screenshot...")

    try:
        photo = await take_screenshot(url, full)
        if not photo:
            return await m.edit("Failed to take screenshot.")

        m = await m.edit("Uploading...")

        await message.reply_photo(photo)
        await m.delete()
    except Exception as e:
        await m.edit(str(e))
