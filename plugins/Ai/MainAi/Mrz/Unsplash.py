from pyrogram import Client, filters
import requests
import asyncio
from datetime import datetime
from pytz import timezone

# Safone API endpoint
SAFONE_API_URL = "https://api.safone.dev/unsplash"
# Animation Sticker ID
STICKER_ID = "CAACAgQAAxkBAAIav2aJXr9WgCsyzWEVNPfs1352ByujAAJuDwAC4eqxUNoxB5joJxGiHgQ"

# Function to handle /unsplash command
@Client.on_message(filters.command("unsplash"))
async def unsplash_search(client, message):
    # Extract query from the message
    query = " ".join(message.command[1:])
    if not query:
        await message.reply_text("Please provide a search query.")
        return
    
    # Send animation sticker to show processing
    sticker_message = await message.reply_sticker(STICKER_ID)
    
    try:
        # Call the Safone Unsplash API
        response = requests.get(f"{SAFONE_API_URL}?query={query}")
        response.raise_for_status()  # Raises HTTPError for bad responses

        data = response.json()
        
        if data.get("results"):
            # Simulate delay for animation
            await asyncio.sleep(3)  # Adjust delay time as needed
            
            # Prepare response message with Unsplash search results
            reply_text = f"ʜᴇʏ: {message.from_user.mention}\n\n"
            reply_text += f"ϙᴜᴇʀʏ: {query}\n\n"
            reply_text += f"ʀᴇsᴜʟᴛs:\n\n"
            
            for result in data["results"]:
                image_url = result.get("imageUrl")
                description = result.get("description", "No description")
                title = result.get("title", "No title")
                
                reply_text += f"[{title}]({image_url})\n{description}\n\n"
            
            # Add current date and time (IST)
            ist = timezone('Asia/Kolkata')
            current_datetime = datetime.now(ist)
            
            reply_text += (f"Date and Time (IST): {current_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n\n"
                           f"Provided by @Mrz_bots")
            
            # Edit the sticker message to show the final result
            await sticker_message.delete()  # Delete the sticker message
            await message.reply_text(reply_text, disable_web_page_preview=True)
        
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
