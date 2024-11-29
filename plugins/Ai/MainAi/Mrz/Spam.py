import aiohttp
import asyncio
from pyrogram import Client, filters

# Asynchronous function to check if a message is spam
async def get_spam_details(message):
    url = "https://api.safone.dev/spam"
    params = {"message": message}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            result = await response.json()
            return result['data']

# Handler for the /checkspam command
@Client.on_message(filters.command("checkspam") & filters.text)
async def check_spam(client, message):
    if len(message.command) < 2:
        await message.reply("Please provide a message to check. Usage: /checkspam <your_message>")
        return

    text_to_check = ' '.join(message.command[1:])
    spam_details = await get_spam_details(text_to_check)
    
    response_message = (
        f"Spam Check Result:\n"
        f"Ham: {spam_details['ham']}\n"
        f"Is Spam: {spam_details['is_spam']}\n"
        f"Model Accuracy: {spam_details['model_accuracy']}%\n"
        f"Profanity: {spam_details['profanity']}\n"
        f"Spam: {spam_details['spam']}\n"
        f"Spam Probability: {spam_details['spam_probability']}"
    )
    
    await message.reply(response_message)
