from pyrogram import Client, filters
import aiohttp
from datetime import datetime
import pytz
import asyncio

@Client.on_message(filters.command("pro"))
async def ask(bot, message):
    # Determine the query
    if message.reply_to_message and message.reply_to_message.text:
        query = message.reply_to_message.text
    else:
        query_parts = message.text.split(" ", 1)
        if len(query_parts) == 1:
            await message.reply("Give An Input!!")
            return
        query = query_parts[1]
    
    # Prepare data with expanded information
    current_date = datetime.now().strftime('%Y-%m-%d')
    data = {
        'query': query,
        'botname': 'Mr.Tom',
        'owner': 'MMW BOTZ',
        'What is your name?': "I'm called Mr.Tom. I was developed to give you information, complete tasks, and assist you in various manners. Provided by @MRXSUPPORTS",
        'Who is MMW BOTZ?': "MMW BOTZ is an exceptionally skilled developer and my guardian in this realm. While I wasn’t initially a coder, I’ve gained expertise in AI programming. I admire Rohit Sharma, known as 'Hitman,' for his remarkable batting, and Jasprit Bumrah for his outstanding bowling. Additionally, COOLTECH is active on YouTube. Provided by @Mrz_bots.",
        'Who is your owner?': "My owner is @aktelegram1. I am an AI assistant programmed to deliver information, execute tasks, and provide multifaceted assistance. Provided by @MRXSUPPORTS.",
        'Who developed you?': f"I am Mr.Tom, created by @MRXSUPPORTS and managed by @aktelegram1. I have been operational since {current_date}. Provided by @MRXSUPPORTS.",
        'What is the date today?': f"Hello! I'm Mr.Tom, your AI assistant developed by @aktelegram1. According to my advanced systems, today's date is: {current_date}. If you need more information about a specific date or want to schedule an event or reminder, just let me know!",
        'What is Mr.Tom?': "Mr.Tom is a helpful assistant developed by @aktelegram1. I’m here to assist you with a wide range of tasks and provide information on various topics. Let me know how I can help you today.",
        'What is MMW BOTZ?': "MMW BOTZ is a highly skilled AI developer with expertise in HTML, Python, and JavaScript. They work on various AI applications, using technical data to enhance projects and collaborate with others. Active on GitHub, MMW BOTZ shares knowledge, collaborates on initiatives, and is committed to learning new technologies and improving programming skills. Always eager to help, COOLTECH embraces opportunities to grow and share expertise.",
        '@aktelegram1': "@aktelegram1 is a skilled developer and his GitHub ID is https://github.com/mallu-movie-world-dev1. You can contact him on Telegram at @aktelegram1.",
        '@Kevinbotmallubot': "The powerful autofilter bot, @Kevinbotmallubot, boasts numerous impressive features. It was developed by @aktelegram1, who can be contacted on Telegram at @aktelegram1."
    }
    
    # Send initial sticker
    m = await message.reply_sticker("CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ")
    
    # Delay for 2 seconds
    await asyncio.sleep(2)
    
    # Make the API request
    url = "https://horrid-api.vercel.app/aipro"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url, json=data) as response:
                response_data = await response.json()
                if 'response' not in response_data:
                    await message.reply("The API did not return the expected data.")
                    return
        except Exception as e:
            await message.reply(f"An error occurred: {e}")
            return
    
    # Get current datetime in IST
    ist = pytz.timezone('Asia/Kolkata')
    current_datetime = datetime.now(ist).strftime('%Y-%m-%d %H:%M:%S')

    # Format the response
    formatted_response = (
        f"ʜᴇʏ: {message.from_user.mention}\n\n"
        f"ϙᴜᴇʀʏ: {query}\n\n"
        f"ʀᴇsᴜʟᴛ:\n\n{response_data['response']}\n\n"
        f"Date and Time (IST): {current_datetime}\n\n"
        f"Provided by @MRXSUPPORTS"
    )
    
    # Delete the sticker message and send the response
    await m.delete()
    await message.reply_text(formatted_response)
