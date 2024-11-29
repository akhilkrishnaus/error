from pyrogram import Client, filters
import requests
import asyncio
from datetime import datetime
import pytz

@Client.on_message(filters.command("news"))
async def latest_news(client, message):
    try:
        query = message.text.split(" ", 1)[1]  # get the query from the message
    except IndexError:
        await client.send_message(chat_id=message.chat.id, text="Please provide a news topic to search for.")
        return

    # Send the sticker first
    sticker_message = await message.reply_sticker("CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ")

    # Simulate delay time for fetching data
    await asyncio.sleep(3)  # Adjust delay time as necessary

    response = requests.get(f"https://horrid-api.onrender.com/news?query={query}")
    if response.status_code == 200:
        news_data = response.json()
        news_title = news_data.get("title")
        news_source = news_data.get("source")
        news_url = news_data.get("url")
        
        # Get the current date and time in IST
        ist = pytz.timezone('Asia/Kolkata')
        current_datetime = datetime.now(ist)

        news_text = (
            f"📰 Latest News:\n\n"
            f"Title: {news_title}\n"
            f"Source: {news_source}\n"
            f"URL: {news_url}\n\n"
            f"Date and Time (IST): {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
            f"Provided by @Mrz_bots"
        )
    else:
        news_text = "Failed to fetch the latest news. Please try again later."

    # Delete the sticker message
    await sticker_message.delete()

    # Send the news_text as a new message
    await client.send_message(chat_id=message.chat.id, text=news_text)
