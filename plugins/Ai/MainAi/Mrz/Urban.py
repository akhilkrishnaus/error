import requests
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from datetime import datetime
from pytz import timezone

# Safone API endpoint
SAFONE_API_URL = "https://api.safone.dev/urban"
# Animation Sticker ID
STICKER_ID = "CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ"

# Function to handle /urban command
@Client.on_message(filters.command("urban"))
async def urban_search(client: Client, message: Message):
    # Get the query from the command arguments
    query = message.text.split(maxsplit=1)[1] if len(message.text.split()) > 1 else None
    
    if query:
        # Send animation sticker to show processing
        sticker_message = await message.reply_sticker(STICKER_ID)
        
        try:
            # Make a request to the Safone Urban Dictionary API
            response = requests.get(f"{SAFONE_API_URL}?query={query}")
            response.raise_for_status()  # Raises HTTPError for bad responses

            data = response.json()
            
            if "results" in data and data["results"]:
                # Simulate delay for animation
                await asyncio.sleep(3)  # Adjust delay time as needed

                # Prepare response text
                response_text = f"ʜᴇʏ: {message.from_user.mention}\n\n"
                response_text += f"ϙᴜᴇʀʏ: {query}\n\n"
                response_text += f"ʀᴇsᴜʟᴛs:\n\n"
                
                # Extract and format the results
                for result in data["results"][:5]:  # Limit to the first 5 results
                    response_text += (
                        f"**Word:** {result['word']}\n"
                        f"**Author:** {result['author']}\n"
                        f"**Date:** {result['date']}\n"
                        f"**Definition:** {result['definition']}\n"
                        f"**Example:** {result['example']}\n"
                        f"**Likes:** {result['likes']} | **Dislikes:** {result['dislikes']}\n"
                        f"**Link:** {result['link']}\n\n"
                    )
                
                # Add current date and time (IST)
                ist = timezone('Asia/Kolkata')
                current_datetime = datetime.now(ist)
                response_text += (f"Date and Time (IST): {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                                  f"Provided by @Mrz_bots")
                
                # Edit the sticker message to show the final result
                await sticker_message.delete()  # Delete the sticker message
                await message.reply_text(response_text, disable_web_page_preview=True)
            
            else:
                await sticker_message.delete()
                await message.reply_text("No results found.")
        
        except requests.exceptions.RequestException as e:
            await sticker_message.delete()
            await message.reply_text(f"Error: {e}")
        
        except (KeyError, ValueError) as e:
            await sticker_message.delete()
            await message.reply_text(f"Error processing API response: {e}")
        
        except Exception as e:
            await sticker_message.delete()
            await message.reply_text(f"Unexpected error: {e}")
    
    else:
        await message.reply_text("Please provide a word to search.")
