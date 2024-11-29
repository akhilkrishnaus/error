from pyrogram import Client, filters
import requests
import asyncio

# Define an asynchronous message handler
@Client.on_message(filters.command("gnews"))
async def global_news(client, message):
    try:
        # Send the sticker first
        sticker_message = await message.reply_sticker("CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ")
        
        # Simulate delay time for fetching data
        await asyncio.sleep(2)  # Adjust delay time as necessary

        response = requests.get("https://api.safone.dev/news")
        if response.status_code == 200:
            news = response.json()
            articles = news.get('results', [])
            news_message = ""
            for article in articles:
                title = article.get("title", "No title")
                description = article.get("description", "No description")
                url = article.get("link", "No URL")
                news_message += f"**Title:** {title}\n**Description:** {description}\n**URL:** {url}\n\n"
            if news_message:
                await sticker_message.edit_text(news_message)  # Ensure to await here
            else:
                await sticker_message.edit_text("No news available at the moment.")  # Ensure to await here
        else:
            await sticker_message.edit_text("Failed to fetch news.")  # Ensure to await here
    except Exception as e:
        await sticker_message.edit_text(f"An error occurred: {e}")  # Ensure to await here
        print(f"Error occurred: {e}")
