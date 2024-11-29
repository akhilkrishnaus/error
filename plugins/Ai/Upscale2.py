from pyrogram import Client, filters
from Mangandi import ImageUploader
import requests 

api_key = "horridapi_x_MwSgfdx9rsoF4pIjMw5Q_free_key"

num = 8

@Client.on_message(filters.command("upscale"))
async def upscale(bot, m):
    if not m.reply_to_message.photo:
        await m.reply_text("Rᴇᴘʟʏ ᴛᴏ ᴀ ᴘʜᴏᴛᴏ ᴛᴏ ᴜꜱᴇ ᴛʜɪꜱ ᴄᴏᴍᴍᴀɴᴅ!")
        return
 
    if m.reply_to_message.photo:
        s = await m.reply_text("Dᴏᴡɴʟᴏᴅɪɴɢ...")
        download = await m.reply_to_message.download()
        await s.edit("Uᴘʟᴏᴀᴅɪɴɢ...")
        media = ImageUploader(download)
        photo = media.upload()       
        response = requests.get(f"https://horridapi.onrender.com/upscale?api_key={api_key}&url={photo}&scale={num}")
        data = response.json()
        
        if not data["STATUS"] == "OK":
            await s.edit(f"Aɴ Oᴄᴄᴜʀᴇᴅ Eʀʀᴏʀ: {data['error']}")

        if data["STATUS"] == "OK":
            await bot.send_document(chat_id=m.chat.id, document=data["data"][0]["URL"], caption="Sᴜᴄᴄᴇꜱꜱғᴜʟʟʏ Uᴘꜱᴄᴀʟᴇᴅ")
