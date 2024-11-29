from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.command("groupinfo", prefixes="/"))
async def get_group_status(client: Client, message: Message):
    if len(message.command) != 2:
        await message.reply("Please provide a group username. Example: /groupinfo YourGroupUsername")
        return
    
    group_username = message.command[1]
    
    try:
        # Use the username to get the chat
        group = await client.get_chat(group_username)
    except Exception as e:
        await message.reply(f"Error: {e}")
        return
    
    total_members = await client.get_chat_members_count(group.id)
    group_description = group.description or 'N/A'  # Default to 'N/A' if description is None
    premium_acc = banned = deleted_acc = bot = 0  # Placeholder for actual counts

    response_text = (
        f"➖➖➖➖➖➖➖\n"
        f"➲ GROUP NAME : {group.title} ✅\n"
        f"➲ GROUP ID : {group.id}\n"
        f"➲ TOTAL MEMBERS : {total_members}\n"
        f"➲ DESCRIPTION : {group_description}\n"
        f"➲ USERNAME : @{group_username}\n"
        f"➖➖➖➖➖➖➖"
    )
    
    await message.reply(response_text)
