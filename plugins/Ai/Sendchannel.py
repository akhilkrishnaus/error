from pyrogram import Client, filters, enums
from pyrogram.types import *
from pyrogram.errors import *
import asyncio

async def send_messages(group_id, message):
        idd=await message.copy(chat_id=group_id)
        messageid = idd.id
        return messageid

@Client.on_message(filters.command("get_id"))
async def get_i_d(client:Client, message:Message):
 try:
    chat_type = message.chat.type
    msg = message.text
    if chat_type in [enums.ChatType.CHANNEL, enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        ids = message.chat.id
        r=await message.reply(f"<code>/send {ids}</code>\n\ncopy this command and reply to the post that you wanna to send to your channel. This message will delete in 8 seconds.")
        r_id = r.id
        user_msg_id = r_id - 1
        await asyncio.sleep(8) 
        await r.delete()
        xx=await client.get_messages(ids, user_msg_id)
        x = xx.text
        if (x=="/get_id"):
            await client.delete_messages(ids, user_msg_id)
        else:
            pass

    elif chat_type in [enums.ChatType.PRIVATE]:
        await message.reply_text("This command is only work in channel and group.")
 except Exception as e:
         await message.reply_text(e)
    

@Client.on_message(filters.command("tosend") & filters.reply & filters.private)
async def send_msg(client:Client, message:Message):
  try:
    uid = message.from_user.id
    user_id = int(uid)
    group_id = message.text.split()[1::]
    gid = "".join(group_id)
    groupid = int(gid)
    msg = message.reply_to_message

    me = await client.get_me()

    user = await client.get_chat_member(groupid , user_id)
    if user.status not in [enums.ChatMemberStatus.OWNER , enums.ChatMemberStatus.ADMINISTRATOR]:
        await message.reply_text("You are not allowed to use this command")
        return

    bot = await client.get_chat_member(groupid , me.id)
    if bot.status not in [enums.ChatMemberStatus.ADMINISTRATOR]:
        await message.reply_text("Please promote me as admin.")
        return

    m_id = await send_messages(groupid, msg)
    if m_id:
       
        await message.reply_text(f"Success.")
        await client.pin_chat_message(groupid, m_id)
        await client.delete_messages(groupid, m_id+1)
    else:
        await message.reply_text("Something error occured.")
        return
  except Exception as e:
      await message.reply_text(e)
