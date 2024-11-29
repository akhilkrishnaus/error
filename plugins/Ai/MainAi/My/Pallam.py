# credits @Mrz_bots
from pyrogram import Client, filters
import requests
from datetime import datetime
import pytz
import asyncio

@Client.on_message(filters.command("palm"))
async def palm(client, message):
    if len(message.text.split(" ", 1)) == 1:
        return await message.reply_text("Provide a query")
    
    query = message.text.split(" ", 1)[1].strip().lower()
    
    user_full_name = message.from_user.first_name
    if message.from_user.last_name:
        user_full_name += f" {message.from_user.last_name}"
    
    # Get current time in UTC and convert to IST
    utc_now = datetime.now(pytz.utc)
    ist_now = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))
    current_datetime = ist_now.strftime("%Y-%m-%d %H:%M:%S")
    current_date = ist_now.strftime("%Y-%m-%d")
    current_year = ist_now.strftime("%Y")
    
    predefined_responses = {
        "what is your name": "My name is Mr.Tom. I am an AI assistant designed to provide you with information, perform tasks, and assist you in various ways.",
        "who is Albert": "Albert is the very talented developer who acts as my caretaker in this world. I wasn't originally a developer, but I've learned to code in AI. In sports, my favorite cricket players are Rohit Sharma, known as 'Hitman,' for his batting skills, and Jasprit Bumrah for his bowling prowess. COOLTECH is also a YouTuber.",
        "who is your owner": "My owner is @aktelegram1. I am an AI assistant designed to provide you with information, perform tasks, and assist you in various ways.",
        "today date": f"Today's date is {current_date}.",
        "who is your developers": f"You are Mr.Tom, developed by @MRXSUPPORTS, owned by @aktelegram1. You are alive on {current_date} in the year {current_year}."
    }
    
    if query in predefined_responses:
        result = predefined_responses[query]
    else:
        api = f"https://horrid-api.vercel.app/palm?query={query}"
        response = requests.get(api)
        result = response.json().get("result", "No result found")
    
    formatted_response = (
        f"ʜᴇʏ: {user_full_name}\n\n"
        f"ϙᴜᴇʀʏ: {query}\n\n"
        f"ʀᴇsᴜʟᴛ:\n\n{result}\n\n"
        f"Date and Time (IST): {current_datetime}\n\n"
        f"Provided by @MRXSUPPORTS"
    )
    
    sticker = await message.reply_sticker("CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ")
    
    await asyncio.sleep(2)  # Adjust the delay as needed
    
    await sticker.delete()
    await message.reply_text(formatted_response)
