from pymongo import MongoClient
from info import DATABASE_URI
from pyrogram import Client, filters

horrid = MongoClient(DATABASE_URI)
warndb = horrid["warndb"]
warn = warndb["warn_users"]

@Client.on_message(filters.command("warn") & filters.group)
async def warnn(bot, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.text.split(None, 1)[1] 
    
    user = await bot.get_users(user_id)    

    user_stats = await bot.get_chat_member(message.chat.id, message.from_user.id)
    bot_stats = await bot.get_chat_member(message.chat.id, bot.me.id)
    if not bot_stats.privileges:
        return await message.reply("Make me Admin I am not admin in this chat")
        
    elif not user_stats.privileges:
        return await message.reply("You are not admin in this chat")
        
    elif not user_stats.privileges.can_restrict_members:
        return await message.reply_text("You Are Admin, but you don't have warn permission")

    if not await bot.get_chat_member(message.chat.id, user.id):
        await message.reply_text("This user can't be found in this group.")
        return

    warns = warn.find_one({'chat': message.chat.id, 'user_id': user.id})    
    
    if user.id == bot.me.id:
        await message.reply_text("Lol I can't warn myself ðŸ™ƒ")
        return 

    if user.id == 1867106198:
        await message.reply_text("I can't warn my owner")
        return 

    if warns is not None and warns.get("cound", 0) >= 2:  
        await message.chat.ban_member(user.id)
        await message.reply_text(f"Hehe\nWarn is 3. So {user.first_name} has been banned from this chat.")
        return

    reason = message.text.split(None, 2)[2] if len(message.text.split(None)) > 2 else "No reason provided."
    
    if warns is None:  # Updated line
        await message.reply_text(f"!Warn\n\nUser: {user.first_name}\n\nAdmin: {message.from_user.mention}\n\nCount: 1\nReason: {reason}")
        warn.insert_one({'chat': message.chat.id, 'user_id': user.id, 'cound': 1, 'reasons': [reason]})
        return 

    new_count = warns["cound"] + 1 if warns else 1  # Updated line
    
    warn.update_one(
        {'chat': message.chat.id, 'user_id': user.id},
        {'$set': {'cound': new_count}, '$push': {'reasons': reason}},
        upsert=True
    )

    await message.reply_text(f"!Warn\n\nUser: {user.first_name}\n\nAdmin: {message.from_user.mention}\n\nCount: {new_count}\nReason: {reason}")

@Client.on_message(filters.command("warns") & filters.group)
async def warns(bot, message):
    if message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
    else:
        user_id = message.text.split(None, 1)[1] or message.from_user.id

    user = await bot.get_users(user_id)
    warns = warn.find_one({'chat': message.chat.id, 'user_id': user.id})

    if warns and warns.get("cound", 0) > 0:  
        reasons = "\n".join(warns["reasons"])
        await message.reply_text(f"{user.first_name}'s Warns:\nCount: {warns['cound']}\nReasons:\n{reasons}")
    else:
        await message.reply_text(f"{user.first_name} does not have any warns.")
