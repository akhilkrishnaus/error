import requests
from pyrogram import Client, filters
import asyncio

# Function to handle the Google Image Search command
@Client.on_message(filters.command("imagesearch"))
async def image_search(client, message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a search query.")
        return
    
    query = " ".join(message.command[1:])
    url = f"https://api.safone.dev/image?query={query}"

    # Send the animation sticker
    sticker_id = "CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ"
    await message.reply_sticker(sticker_id)
    
    # Wait for a short period to simulate delay
    await asyncio.sleep(2)  # Adjust the delay time as needed

    try:
        response = requests.get(url)
        response.raise_for_status()
        res = response.json()

        # Log the entire JSON response for debugging
        await message.reply_text(f"Full JSON response: {res}")

        if 'data' in res and res['data']:
            images = res['data'][:5]  # Get the top 5 images
            for img in images:
                await message.reply_photo(img['url'], caption=f"Title: {img['title']}\nSource: {img['source']}")
        else:
            await message.reply_text("No images found for your query.")
    except requests.RequestException as e:
        await message.reply_text(f"Request failed: {e}")
    except KeyError:
        await message.reply_text("Unexpected response format.")
