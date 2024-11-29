from pyrogram import Client, filters
import requests
import asyncio
from datetime import datetime
from pytz import timezone
import logging

# Safone API endpoint
safone_api_url = 'https://api.safone.dev/torrent'
# Animation Sticker ID
STICKER_ID = "CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ"

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to handle /search_torrent command
@Client.on_message(filters.command("torrent", prefixes="/"))
async def search_torrent(client, message):
    try:
        # Extract query from message
        query = message.text.split(maxsplit=1)[1]

        # Send animation sticker to show processing
        sticker_message = await message.reply_sticker(STICKER_ID)

        try:
            # Make request to Safone API
            response = requests.get(safone_api_url, params={'query': query})
            response.raise_for_status()  # Raise exception for 4xx/5xx errors

            # Simulate delay for animation
            await asyncio.sleep(5)  # Adjust delay time as needed

            # Process API response
            torrent_data = response.json()
            results = torrent_data.get('results', [])

            if results:
                # Prepare response message with torrent results
                ist = timezone('Asia/Kolkata')
                current_datetime = datetime.now(ist)
                response_text = (f"ʜᴇʏ: {message.from_user.mention}\n\n"
                                 f"ϙᴜᴇʀʏ: {query}\n\n"
                                 f"ʀᴇsᴜʟᴛs:\n\n")

                for result in results[:5]:  # Limit to 5 results
                    response_text += (f"Title: {result['name']}\n"
                                      f"Size: {result['size']}\n"
                                      f"Seeders: {result['seeders']}\n"
                                      f"Leechers: {result['leechers']}\n"
                                      f"Magnet link: {result['magnetLink']}\n\n")

                response_text += (f"Date and Time (IST): {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                                  f"Provided by @Mrz_bots")

                # Edit the sticker message to show the final result
                await sticker_message.delete()  # Delete the sticker message
                await message.reply_text(response_text)

            else:
                await sticker_message.delete()
                await message.reply_text("No torrents found for your query.")

        except requests.exceptions.RequestException as e:
            await sticker_message.delete()
            await message.reply_text(f"Error fetching torrents: {e}")

    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        await message.reply_text("An unexpected error occurred.")
