from pyrogram import Client, filters
import aiohttp
from io import BytesIO
from datetime import datetime
import pytz

# Async function to get QR code image data
async def get_qr_code_image(text):
    url = f"https://horridapi2-0.onrender.com/qr?text={text}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200 and response.content_type == 'image/png':
                image_data = await response.read()
                return image_data
    return None

@Client.on_message(filters.command("qr"))
async def qr_command(client, message):
    if len(message.command) > 1:
        text = " ".join(message.command[1:])
        qr_code_image_data = await get_qr_code_image(text)
        if qr_code_image_data:
            try:
                # Get current date and time in IST
                ist = pytz.timezone('Asia/Kolkata')
                current_datetime = datetime.now(ist)

                await client.send_photo(
                    message.chat.id,
                    BytesIO(qr_code_image_data),
                    caption=f"Here's your QR code, {message.from_user.mention}!\n\nQuery: {text}\n\nDate and Time (IST): {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n𝘗𝘳𝘰𝘷𝘪𝘥𝘦𝘥 𝗯𝘆 @Mrz_bots"
                )
            except Exception as e:
                await message.reply(f"Failed to send QR code image: {e}")
        else:
            await message.reply("Failed to generate QR code.")
    else:
        await message.reply("Please provide text to generate QR code.")
