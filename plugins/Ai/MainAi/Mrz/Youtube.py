import requests
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

# Safone API endpoint for YouTube search
SAFONE_API_URL = "https://api.safone.dev/youtube"
# Animation sticker ID
STICKER_ID = "CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ"

# Command handler for /youtube
@Client.on_message(filters.command("youtube") & filters.private)
async def youtube_search(client: Client, message: Message):
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("Please provide a search query after the /youtube command.")
        return

    # Send animation sticker to show processing
    sticker_message = await message.reply_sticker(STICKER_ID)

    try:
        # Make the API request to Safone YouTube Search API
        api_params = {
            "query": query,
            "limit": 5  # Limiting to 5 results
        }
        headers = {"accept": "application/json"}

        response = requests.get(SAFONE_API_URL, params=api_params, headers=headers)
        response.raise_for_status()  # Raise exception for 4xx/5xx errors
        data = response.json()

        if 'results' in data and data['results']:
            # Simulate delay for animation
            await asyncio.sleep(3)  # Adjust delay time as needed

            results = data['results']
            for result in results:
                video_title = result.get('title', 'No title available')
                video_url = result.get('link', 'No URL available')
                video_description = result.get('descriptionSnippet', [{'text': 'No description available'}])[0]['text']
                view_count = result.get('viewCount', {}).get('text', 'Views not available')

                await message.reply_text(
                    f"**Title:** {video_title}\n"
                    f"**URL:** {video_url}\n"
                    f"**Description:** {video_description}\n"
                    f"**View Count:** {view_count}"
                )
        else:
            await message.reply_text("No results found for your query.")

    except requests.exceptions.RequestException as e:
        await message.reply_text(f"An error occurred: {e}")

    finally:
        # Delete the animation sticker
        await sticker_message.delete()

# Note: Adjust the delay time (asyncio.sleep) as per your preference for how long the animation should display.
