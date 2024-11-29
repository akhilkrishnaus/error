import re, asyncio, os, sys
from pyrogram import Client, filters, enums
from info import ADMINS

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def restart_message(client, message):
    video_msg = await message.reply_video("https://telegra.ph/file/28243fd0e104ddb555e97.mp4", 
                                          caption="🔄𝙍𝙀𝙎𝙏𝘼𝙍𝙏𝙄𝙉𝙂....")
    chat_id = message.chat.id
    await asyncio.sleep(3)
    await video_msg.edit_caption("✅️𝙉𝙊𝙒 𝙔𝙊𝙐 𝘾𝘼𝙉 𝙐𝙎𝙀 𝙈𝙀....")
    await asyncio.sleep(1)  # add a small delay to ensure the caption is updated
    os.execl(sys.executable, sys.executable, *sys.argv)

# Auto-forwarding messages to a specific chat (you can change the destination as needed)
DESTINATION_CHAT_ID = -1002197120480  # Replace with your destination chat ID

async def auto_forward(client, message):
    try:
        # Forward the message to the destination chat
        await client.forward_messages(
            chat_id=DESTINATION_CHAT_ID,  # Destination chat ID
            from_chat_id=message.chat.id,  # Original chat ID
            message_ids=message.message_id  # Message ID to forward
        )
    except Exception as e:
        print(f"Error forwarding message: {e}")

# To run the bot every hour (60 minutes)
async def auto_restart_every_hour():
    while True:
        await asyncio.sleep(3600)  # Sleep for 3600 seconds (1 hour)
        os.execl(sys.executable, sys.executable, *sys.argv)

    # Start the auto-restart task in the background
    loop = asyncio.get_event_loop()
    loop.create_task(auto_restart_every_hour())
