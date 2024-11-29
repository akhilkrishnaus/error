import os
import logging
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import ChatAdminRequired, FloodWait


@Client.on_message(filters.command("banall") & filters.group)
async def banall_command(client, message: Message):
    print("ɢᴇᴛᴛɪɴɢ ᴍᴇᴍʙᴇʀs ғʀᴏᴍ {}".format(message.chat.id))
    banned_count = 0

    async for member in app.get_chat_members(message.chat.id):
        try:
            await devine.ban_chat_member(chat_id=message.chat.id, user_id=member.user.id)
            banned_count += 1
            print("ʙᴀɴɴᴇᴅ {} ғʀᴏᴍ {}".format(member.user.id, message.chat.id))
            await message.reply_text(f"<b>‣ {member.user.mention} ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.</b>")
        except ChatAdminRequired:
            print(f"ʙᴏᴛ ᴅᴏᴇs ɴᴏᴛ ʜᴀᴠᴇ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ɪɴ {message.chat.id}")
            await message.reply_text("<b>‣ ɪ ɴᴇᴇᴅ ᴀᴅᴍɪɴ ʀɪɢʜᴛs ᴛᴏ ʙᴀɴ ᴍᴇᴍʙᴇʀs.</b>")
            break
        except FloodWait as e:
            print(f"ғʟᴏᴏᴅ ᴡᴀɪᴛ ᴏғ {e.x} sᴇᴄᴏɴᴅs")
            await asyncio.sleep(e.x)
        except Exception as e:
            print(f"ғᴀɪʟᴇᴅ ᴛᴏ ʙᴀɴ {member.user.id}: {e}")

    print(f"ᴘʀᴏᴄᴇss ᴄᴏᴍᴘʟᴇᴛᴇᴅ, ᴛᴏᴛᴀʟ {banned_count} ʙᴇᴇɴ ʙᴀɴɴᴇᴅ.")
    await message.reply_text(f"<b>‣ ᴛᴏᴛᴀʟ {banned_count} ᴍᴇᴍʙᴇʀs ʙᴀɴɴᴇᴅ.</b>")
